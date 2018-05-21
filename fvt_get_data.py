# mylib.py
import logging
import paramiko
import re
from collections import defaultdict
import fvt
logger = logging.getLogger(__name__)

def do_something():
    logger.warn('Doing something')

def test1():
    logger.info("how r u ")
    a = {1:2}
    x=[1,2]
    y= [3,4]
    logger.info("or %s", a)
    logger.info("sdfsdf %s",zip(x,y))

def get_flow_table(devicename,podname,obj,dtime,switch_ip):
    command = '/opt/broadcom/ofdpa/bin/client_flowtable_dump'  
    output,obj,flag = fvt.execute_command(command,obj)    
    if output and flag == 0:
        if "daas" not in devicename:
            f = open('logs/'+dtime+'/'+devicename+'_'+podname+'_'+'flow.tables','w')
        else:
            f = open('logs/'+dtime+'/'+switch_ip.rstrip() + 'daas_'+podname+'_'+'flow.tables','w')
        f.write(output)
        f.close()
        logger.info("Successfully created "+ devicename + " flow tables")
    else:
        logger.error("Failed to get the flow tables")
        flag = 1
    return output,obj

def get_group_table(devicename,podname,obj,dtime,switch_ip):
    command = '/opt/broadcom/ofdpa/bin/client_grouptable_dump'  
    output,obj,flag = fvt.execute_command(command,obj)    
    if output and flag == 0:
        if "daas" not in devicename:
            f = open('logs/'+dtime+'/'+devicename+'_'+podname+'_'+'group.tables','w')
        else:
            f = open('logs/'+dtime+'/'+switch_ip.rstrip() + 'daas_'+podname+'_'+'group.tables','w')
        f.write(output)
        f.close()
        logger.info("Successfully created "+ devicename + " group tables")
    else:
        logger.error("Failed to get the group tables")
        flag = 1
    return output,obj

def get_netcfg(podname,obj):
    command='netcfg'
    output,obj,flag = fvt.execute_command(command,obj)
    if output and flag == 0:
        #f = open('logs/'+dtime+'/netcfg_'+podname+'.conf','w')
        f = open('netcfg_'+podname+'.conf','w')
        f.write(output)
        f.close()
        logger.info("Successfully created netcfg file")
    else:
        logger.error("Failed to get the netcfg file")
        flag = 1
    return output,obj,flag

def get_vcmts_onos_pod_details(obj):
    command = 'kubectl get pods --all-namespaces -o wide|grep -v Unknown'
    ns = []
    pod = []
    vcns = []
    poddict1 = {}
    vcmtspoddict = {}
    poddict = defaultdict(list)
    #poddict = {}
    flag = 1
    output,obj,flag = fvt.execute_command(command,obj)
    if output and flag == 0:
        #print output
        logger.info("List of Kubectl Namespaces and their respective Pod Details \n" + output)
        output1 = output.splitlines()
        for eachline in output1:
            #print eachline
            if re.search(r'onos\-\w*\d[\-\d]*',eachline) or re.search(r'vcmts\-cd[\-\d]+',eachline) or re.search (r'pg[\-\d]+',eachline):
                #print "eachline in pod" + eachline
                ns.append(eachline.split()[0])
                pod.append(eachline.split()[1])
            if re.search(r'vcmts\-cd[\-\d]+',eachline) or re.search(r'pg[\-\d]+',eachline):
                poddict1[eachline.split()[1]] = eachline.split()[7]
                vcmtspoddict.setdefault(eachline.split()[0],{}).update(poddict1)
        if pod:   
            for ns1,pod1 in zip(ns,pod):
                poddict[ns1].append(pod1)
            flag = 0 
            logger.info("VCMTS and ONOS POD Details in each namespace\n %s" , poddict)
        else:
            logger.error("VCMTS and ONOS PODs are not available in Kube Master \n" + output1)      
            flag = 1
    else:
        logger.error("Failed to execute Kubectl Command ' " + command + " '")
        flag = 1        
    return poddict,obj,flag,vcmtspoddict

def get_onos_controller_ip(poddetails,obj,pod_lcce_rpd_map):
    podcontoller = defaultdict(list)
    for namespace,pod in poddetails.items():
        if namespace in pod_lcce_rpd_map.keys():
            for pod1 in pod:
                #logging.info(" ONOS container name -> " + pod1 + " , pod -> " + namespace)
                if re.match(r'onos\-\w*\d[\-\d]*',pod1):
                    command = "kubectl exec "+  pod1 + " -n " + namespace + " ifconfig bond0|grep 'inet addr:' | awk -F'[: ]+' '{ print $4 }'"
                    output,obj,flag = fvt.execute_command(command,obj)
                    if output and flag == 0:
                        #logger.info("Controller ip details " + output)
                        #ip=output.split('\n')[0]
                        ip=output.rstrip()                
                        podcontoller.setdefault(namespace,[]).append(ip)  
                    else:
                        logger.error("Failed to execute command "+command) 
        else:
            logger.info("No RPD's availbale in " + namespace)                  
    return podcontoller,obj,flag
