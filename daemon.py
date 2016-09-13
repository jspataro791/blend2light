
# BLEND2LIGHT DAEMON
# This daemon listens for Blender's output
# and sends info over DMX

import socket
import sys

#### DEFAULTS ####

DEF_SOCKET = 8081
DEF_IP = 'localhost'

#### GLOBALS ####




####### FUNCTIONS #######

# Open UDP port with Blender
def OpenUDP(ip,port):
	print("Opening UDP on %s:%s" % (repr(ip),repr(port)))
	UDP_IP = ip
	UDP_PORT = port
	
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setblocking(0)
		sock.bind((UDP_IP, UDP_PORT))
	except:
		print("ERR: Unable to open socket on %s:%s" % (repr(ip),repr(port)))
		exit


# Get and parse lamp data
def GetUDPData(socket):
	print("Not yet implemented")


######### MAIN ###########
def main():
	
	
		



if __name__ == "__main__":
	main()
