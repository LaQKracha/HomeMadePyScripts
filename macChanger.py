import subprocess
import optparse
import re
import random

def last_mac(interface):
    ifconf = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    l_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconf)
    if l_mac:
        print(f"MAC before change: {l_mac.group(0)}")
    else:
        print("[-] Unable to get last MAC address")

def get_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def change_mac(interface, mac):
	subprocess.call(["ifconfig", interface, "down"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	subprocess.call(["ifconfig", interface, "hw", "ether", mac], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	subprocess.call(["ifconfig", interface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	subprocess.call(["ifconfig", interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address")
    parser.add_option("-r", "--random", action="store_true", dest="random", help="Generate a random MAC address")
    parser.add_option("-m", "--mac", dest="mac", help="The new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please provide an interface. Use --help for more info.")
    if options.random and options.mac:
        parser.error("[-] You cannot use both -r (--random) and -m (--mac) options together.")
    if options.random and not options.mac:
        options.mac = get_random_mac()
    if not options.mac:
        parser.error("[-] Please provide a MAC address or use the -r (--random) option to generate one.")
    return options

def success(interface, mac):
    ifconfig = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    mac_s = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    if mac_s:
        print(mac_s.group(0))
        if mac_s.group(0) == mac:
            print("[+] Success :)")
        else:
            print("[-] Failure :(")
            print("Try to run me with sudo")
    else:
        print("[-] Could not read MAC address")

if __name__ == '__main__':
    try:
        options = get_arguments()
        last_mac(options.interface)
        if options.random:
            mac = get_random_mac()
        else:
            mac = options.mac
        if mac:
            print(f"[+] Changing MAC address for {options.interface} to {mac}")
            change_mac(options.interface, mac)
            success(options.interface, mac)
            print("[/] Done!")
        else:
            print("[-] Failed to generate a random MAC address.")
    except IndexError:
        print("[-] Something went wrong")
