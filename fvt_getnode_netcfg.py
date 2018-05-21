#! /usr/bin/python
import hashlib
import os
import logging
logger = logging.getLogger(__name__)

SubstrList = ["Leaf","SPINE","DAAS"]
SubstrList1 = ["Leaf","SPINE","DAAS"]
Node_name = {"leaf1a":"Leaf-1A","leaf1b":"Leaf-1B","leaf3a":"Leaf-3A","leaf3b":"Leaf-3B","spinea":"SPINE1","spineb":"SPINE2", "daas1":"DAAS1","daas2":"DAAS2","daas3":"DAAS3","daas4":"DAAS4"}
Daas_cnt = ["DAAS1","DAAS2","DAAS3","DAAS4"]
ipandmac = ["ipv4Loopback", "ipv6Loopback", "routerMac","ipv6NodeSid",]
Spine1A_Name = ["SPINE1","SPINEA"]
Spine2B_Name = ["SPINE2", "SPINEB"]
DAAS_Subnet = []

def get_daas_mac_by_ip(ppod,swtchip):
    ppod = ppod + ".conf"
    test =""
    flag = get_DAAS_cnt(ppod)
    #print "daas count " , flag
    with open(ppod) as fn:
        for line in fn:           
            if "DAAS" in line:
                ipormac = next(fn) 
                if ipormac.find("ipv4")!=-1:
                   ipv4 = ipormac.split("=")
                   #logger.info("printing ipv4 address %s",ipv4[1])
                   test = ipv4[1]
                   if test.rstrip() == swtchip:
                        #elif intrfce == "Mac":
                        next(fn)    
                        next(fn) 
                        ipormac = next(fn)
                        if ipormac.find("Mac")!=-1:
                            Mac = ipormac.split("=")
                            return Mac[1]
        fn.close() 	

def rm_dup_entry(files):
    fnl_file =  files.split("_")
    fnlSwtchcfg = open(fnl_file[1],"w")
    cmp_ln_hash =set()
    for line in open("switchcfg.conf","r"):
        hshvalue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        if hshvalue not in cmp_ln_hash:
            fnlSwtchcfg.write(line)
            cmp_ln_hash.add(hshvalue)
        elif line.find("Mac" or "ipv4" or "ipv6")!=-1:
            fnlSwtchcfg.write(line)
    fnlSwtchcfg.close()
    
def get_swtch_name(ppod,swtchname):
    with open(ppod) as fd:
        for line in fd:
            if(swtchname =="spinea"):
                for spine in Spine1A_Name :
                    if(line.find(spine)!=-1):
                        return line
            if(swtchname =="spineb"):
                for spine in Spine2B_Name :
                    if(line.find(spine)!=-1):
                        return line        
    fd.close()
    


def get_daas_subnets(ppod):
    ppod = ppod + ".conf"
    with open(ppod) as fn:
        for i,line in enumerate(fn,1):
            if line.find("DAAS_Subnet")!=-1: 
                try:             
                    return next(fn)
                except StopIteration:
                     return " "
def get_DAAS_cnt(ppod):
    flag =0
    with open(ppod) as fd:
        for line in fd:
            for cnt in Daas_cnt:
              if(line.find(cnt)!=-1):
                  return 1
    fd.close()
    return flag

def get_node_data(ppod,swtchnme,intrfce):
    ppod = ppod + ".conf"
    flag = get_DAAS_cnt(ppod)
    #print "daas count " , flag
    with open(ppod) as fn:
        for line in fn:
            find_sdr = Node_name[swtchnme]
            #print find_sdr
            if(swtchnme == "spinea")or (swtchnme =="spineb"):
                find_sdr = get_swtch_name(ppod,swtchnme)  
                 
            if(swtchnme =="daas1"):
                if(flag==0):
                    find_sdr ="DAAS"
            if line.find(find_sdr)!=-1:
               if(intrfce=="ipv4"):
                   ipormac = next(fn) 
                   if ipormac.find("ipv4")!=-1:
                       ipv4 = ipormac.split("=")
                       #logger.info("printing ipv4 address %s",ipv4[1])
                       return ipv4[1]
                    
               elif intrfce == "mpls":
                   next(fn)
                   ipormac = next(fn)
                   if ipormac.find("Sid")!=-1:
                       mpls = ipormac.split("=")
                       #print mpls[1]
                       return mpls[1]
               elif intrfce == "ipv6":
                   ipv6fnl=[]
                   next(fn)
                   next(fn)    
                   ipormac = next(fn) 
                   if ipormac.find("ipv6")!=-1:
                       ipv6 = ipormac.split("=")
                       ipv6rm0 = ipv6[1].lower().split(":")
                       for list in ipv6rm0:  
                           ipv6fnl.append(str(list.lstrip("0")) + ":")
                   ipv6mfnl= ''.join(ipv6fnl) 
                   return ipv6mfnl.rstrip(":")
                        
               elif intrfce == "Mac":
                   next(fn)    
                   next(fn) 
                   next(fn)
                   ipormac = next(fn)
                   if ipormac.find("Mac")!=-1:
                       Mac = ipormac.split("=")
                       return Mac[1]
        fn.close()                
                       

def Dup_RPD(RPDip6):
    
    if RPDip6 not in DAAS_Subnet:
        DAAS_Subnet.append(RPDip6)
'''
def get_swtchname_by_of(ppod,of):
    file_name = "netcfg_"+ppod+".txt" 
    with open(file_name) as fp:
        for i,line in enumerate(fp,1):
            if of in line:
                temp = next(fp)                
                if(temp.find("basic")!=-1):
                    next(fp)
                    name =next(fp)
                    name =name.split(":")
                    name = name[1].rstrip('"').lstrip('"')
                    for key, value in Node_name.iteritems():
                        if (name.find(value)!=-1):
                            return key
                if(temp.find("segmentrouting")!=-1):
                    name =next(fp)
                    name =name.split(":")
                    name = name[1].rstrip('"').lstrip('"')
                    for key, value in Node_name.iteritems():
                        if (name.find(value)!=-1):
                            return key              
    fp.close()
    '''
def get_node_interface_data():
    pattern = 'netcfg_ppod'
    path = os.getcwd()
    line1 = 0
    for files in os.listdir(path):
        if files.startswith(pattern):
            with open(files) as fn:
                Swtchcfg = open("switchcfg.conf","w+")   
                Swtchcfg.write ("# Switch Details \n")
                for ln in fn:
                    if "RPD" in ln:                        
                        next (fn)
                        x =next(fn)
                        RPDip = x.split()
                        RPDip[4].rstrip('",').lstrip('"')
                        RPDipv6 = RPDip[4].split('::')                        
                        Dup_RPD (RPDipv6[0].lstrip('"'))
            fn.close()
            with open(files) as fp:
                Swtchcfg = open("switchcfg.conf","w+")   
                Swtchcfg.write ("# Switch Details \n")
                for line in fp:
                    if "segmentrouting" in line:
                        line1=1
                    if line1==1:
                        if "name" in line:
                            SwtchName = line.split()
                            for substr in SubstrList:            
                                if SwtchName[2].find(substr)!=-1:
                                    #print SwtchName[2].rstrip('",').lstrip('"')
                                    Swtchcfg.write ("\n" + SwtchName[2].rstrip('",').lstrip('"')+"\n")
                        for imsub in ipandmac:
                            if imsub in line:
                                IpMacName = line.split()
                                #print (imsub + "="+ IpMacName[2].rstrip('",').lstrip('"')+"\n")
                                Swtchcfg.write (imsub + "="+ IpMacName[2].rstrip('",').lstrip('"')+"\n") 
                        if line.find('}')!=-1:
                            line1=0
                            continue;
            fp.close();                
            Swtchcfg.write("\n[DAAS_Subnet]\n")
            for ipv6 in DAAS_Subnet:
                Swtchcfg.write("%s " % ipv6)
                
            Swtchcfg.close()
            rm_dup_entry(files)
            ppod_name = files.split('_')
            ppod_name = ppod_name[1].split('.')            
            get_node_data(ppod_name[0], "leaf1a","ipv4")
            
get_node_interface_data()
 

      

