import nmap


def scanTop1000(host):  
	# Create a port scanner object
	nm = nmap.PortScanner()

	# Scan localhost for open ports
	nm.scan(host, '1-1024')

	# Iterate over scanned hosts
	for host in nm.all_hosts():
		print('----------------------------------------------------')
		print('Host : %s (%s)' % (host, nm[host].hostname()))
		print('State : %s' % nm[host].state())

	# Iterate over all scanned ports for the host
	for proto in nm[host].all_protocols():
		print('----------')
		print('Protocol : %s' % proto)

	# Get a list of open ports and print them
	port_list = nm[host][proto].keys()
	for port in port_list:
		print('Port : %s\tState : %s' % (port, nm[host][proto][port]['state']))


if __name__ == '__main__':
    scanTop1000('www.phase.com')
    #results = { "results": {"openport1": 443, "openport2": 22, "openport3": 80}  }
    
