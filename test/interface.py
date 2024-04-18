# Import libraries 
import netifaces 

# Getting interfaces 
interfaces = netifaces.interfaces()

# Showing interfaces 
for interface in interfaces: 
	print(interface, ':', netifaces.ifaddresses(interface).get(netifaces.AF_INET)) 