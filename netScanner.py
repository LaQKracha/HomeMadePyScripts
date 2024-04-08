import scapy.all as s
import argparse
import sys

def outPutHeader(clients):
    print("IP\t\t\tMAC Addr\tOS based on TTL\n------------------------------------------------------------------------------------------")
    for client in clients:
        print(f"{client['ip']}\t{client['mac']}\t{client.get('os', 'Unknown')}")

def scan(target, iface):
    arp_req = s.ARP(pdst=target)
    broadcast = s.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_br = broadcast/arp_req
    answered = s.srp(arp_req_br, iface=iface, timeout=1, verbose=False)[0]
    clients = []
    for e in answered:
        c_dict = {"ip": e[1].psrc, "mac": e[1].hwsrc}
        try:
            c_dict['os'] = detect_os(e[1].ttl)
        except Exception as e:
            pass
        clients.append(c_dict)
    return clients

def detect_os(ttl):
    if ttl == 128:
        return "Windows"
    elif ttl == 64:
        return "Linux/Unix"
    elif ttl == 255:
        return "macOS or Router/Firewall"
    else:
        return "Unknown"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="The target IP/mask")
    parser.add_argument("-i", "--iface", dest="iface", help="The network interface to use")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please specify an IP address using -t or --target.")
    return args.target, args.iface

if __name__ == '__main__':
    try:
        target, iface = get_arguments()
        clients = scan(target, iface)
        outPutHeader(clients)
    except Exception as e:
        print("Error:", e)
