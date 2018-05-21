#! /usr/bin/env python
from OFDPA_python import *
from socket import *
from _OFDPA_python import *
import _OFDPA_python
import socket
import struct
import sys
import commands

def main():
        rc = ofdpaClientInitialize("OFDPA_port_example")
        print rc
        if rc == OFDPA_E_NONE:
        #variables used to set up port status
                print "Entered after OFDPA_E_NONE"
                PortNum = 0
                state = new_uint32_tp()
                nextPortNum = new_uint32_tp()
                currentSpeed = new_uint32_tp()
                maxSpeed = new_uint32_tp()
                currSpeed = new_uint32_tp()
                #print "This is the name of the script: ", sys.argv[0]
                #print "Number of arguments: ", len(sys.argv)
                #print "The arguments are: " , str(sys.argv)
                #name = input("Select 1 if you want to display status of all ports else 2 for specific port ")
                text = commands.getstatusoutput("onlpdump -s | grep 'Serial Number' | awk -F'[: ]+' '{ print $4 }'")
                print text
                text1 = text[1]
                print text1
                text2 = text1[:4]
                print text2

                dictleaf = {1: 'MS', 2: 'MS',3: 'MS',4: 'MS',5: 'MS',6: 'MS',7: 'MS',8: 'MS',9: 'MS',10: 'MS',11: 'MS',12: 'MS',13: 'MS',14: 'MS',15: 'MS',16: 'MS',17: 'MS',18: 'MS',19: 'MS',20: 'MS',21: 'MS',22: 'MS',23: 'MS',24: 'MS',25: 'MS',26: 'MS',27: 'MS',28: 'MS',29: 'MS',30: 'MS',31: 'MS',32: 'MS',33: 'MS',34: 'MS',35: 'MS',36: 'MS',37: 'MS',38: 'MS',39: 'MS',40: 'MS',41: 'MS',42: 'MS',43: 'MS',44: 'MS',45: 'MS',46: 'MS',47: 'MS',48: 'MS',49: 'SPINEA',50: 'SPINEA',52: 'SPINEB',53: 'SPINEB'}

                dictspine = {'1': 'DAAS1', '2': 'DAAS2', '3': 'DAAS3','4': 'DAAS4','5': 'MS','6': 'MS','7': 'MS','8': 'MS','9': 'MS','10': 'MS','11': 'MS','12': 'MS','13': 'MS','14': 'MS','15': 'MS','16': 'MS','17': 'LEAF1A','18': 'LEAF1A','19': 'MS','20': 'MS','21': 'LEAF3A','22': 'LEAF3A','23': 'MS','24': 'MS','25': 'LEAF1B','26': 'LEAF1B','27': 'MS','28': 'MS','29': 'LEAF3B','30': 'LEAF3B','31': 'MS','32': 'MS'}

                dictdaas = {'1': 'DAAS1', '2': 'DAAS2', '3': 'DAAS3','4': 'DAAS4','5': 'MS','6': 'MS','7': 'MS','8': 'MS','9': 'MS','10': 'MS','11': 'MS','12': 'MS','13': 'MS','14': 'MS','15': 'MS','16': 'MS','17': 'LEAF1A','18': 'LEAF1A','19': 'MS','20': 'MS','21': 'LEAF3A','22': 'LEAF3A','23': 'MS','24': 'MS','25': 'LEAF1B','26': 'LEAF1B','27': 'MS','28': 'MS','29': 'LEAF3B','30': 'LEAF3B','31': 'MS','32': 'MS','33': 'MS','34': 'MS','35': 'MS','36': 'MS','37': 'MS','38': 'MS','39': 'MS','40': 'MS','41': 'MS','42': 'MS','43': 'MS','44': 'MS','45': 'MS','46': 'MS','47': 'MS','48': 'MS','49': 'SPINEA','50': 'SPINEB'}

                if len(sys.argv) == 1:
                        rc = ofdpaPortNextGet(PortNum,nextPortNum)
                        print 'PortNo:\t PortState:\t PortStatus:'
                        while rc == OFDPA_E_NONE:
                                rc1 = ofdpaPortStateGet(uint32_tp_value(nextPortNum),state)
                                rc2 = ofdpaPortMaxSpeedGet (uint32_tp_value(nextPortNum),maxSpeed)
                                rc3 = ofdpaPortCurrSpeedGet (uint32_tp_value(nextPortNum),currSpeed)
                                #print 'PortNo:' +str(uint32_tp_value(nextPortNum))+   '\t\t currSpeed :' +str(uint32_tp_value(currSpeed))
                                print
                                #print 'PortNo:' +str(uint32_tp_value(nextPortNum))+   '\t\t PortState:' +str(uint32_tp_value(state))
                                #ofdpaPortCurrSpeedGet(portNum, &currentSpeed);
                                state1 = uint32_tp_value(state)
                                print nextPortNum
                                for nextPortNum, v in dictleaf.items():
									if nextPortNum in dictleaf:
										if state1 == 0:
											print 'PortNo:' +str(uint32_tp_value(nextPortNum))+'\t PortState:' +str(uint32_tp_value(state))+'\tOFDPA_PORT_STATUS_ACTIVE' + '\tmaxSpeed : ' +str(uint32_tp_value(maxSpeed))+ '\t currSpeed : ' +str(uint32_tp_value(currSpeed)) + ''
										elif state1 == 1:
											print 'PortNo:' +str(uint32_tp_value(nextPortNum))+'\t PortState:' +str(uint32_tp_value(state))+'\tOFDPA_PORT_STATE_LINK_DOWN' + '\tmaxSpeed : ' +str(uint32_tp_value(maxSpeed))+ '\t currSpeed : ' +str(uint32_tp_value(currSpeed)) + ''
										elif state1 == 2:
											print 'PortNo:' +str(uint32_tp_value(nextPortNum))+'\t\t PortState:' +str(uint32_tp_value(state))+'\t\t\tOFDPA_PORT_STATE_BLOCKED'
										elif state1 == 4:
											print 'PortNo:' +str(uint32_tp_value(nextPortNum))+'\t\t PortState:' +str(uint32_tp_value(state))+'\t\t\tOFDPA_PORT_STATE_LIVE'
											rc = ofdpaPortNextGet(uint32_tp_value(nextPortNum),nextPortNum)
                                        elif len(sys.argv) > 1:
											nextPortNum = new_uint32_tp()
											state = new_uint32_tp()
											#portinput = input("Enter the port numbers which you want to check the status ")
											n = len(sys.argv)
											#print n
											for i in range(1,n):
												#print "Printing n value" ,(sys.argv[i])
												nextPortNum = int(sys.argv[i])
												if nextPortNum in range(1,55):
												#print "Printing nextPortNum",nextPortNum
													while rc == OFDPA_E_NONE:
														rc = ofdpaPortStateGet(nextPortNum,state)
														#print sys.argv[i],uint32_tp_value(state)
														state2 = uint32_tp_value(state)
														if state2 == 0:
																print 'PortNo:' +str(nextPortNum)+'\t\t PortState:' +str(uint32_tp_value(state))+'\t\t\tOFDPA_PORT_STATUS_ACTIVE'
																break
														elif state2 == 1:
																print 'PortNo:' +str(nextPortNum)+'\t\t PortState:' +str(uint32_tp_value(state))+'\t\t\tOFDPA_PORT_STATE_LINK_DOWN'
																break
														elif state2 == 2:
																print 'PortNo:' +str(nextPortNum)+'\t\t PortState:' +str(uint32_tp_value(state))+'\t\t\tOFDPA_PORT_STATE_BLOCKED'
																break
														elif state3 == 4:
																print 'PortNo:' +str(nextPortNum)+'\t\t PortState:' +str(uint32_tp_value(state))+'\t\t\tOFDPA_PORT_STATE_LIVE'
														elif nextPortNum not in range(1,54):
																print "Please give correct input for the switch"
														break



if __name__ == '__main__': main()
