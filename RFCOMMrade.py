#!/usr/bin/env python3
"""
PyBluez RFCOMM Load test application - RFCommrade

This is a poorly designed application to bombard the specified RFCOMM channel at the specified BT Address with lots of data.

The default for this example is a payload of a bunch of '/'s but it could really be anything.

The target device doesn't necessarily have to be paired to use this script, but unless you pair your device to the target, results won't be very interesting.

Requires pybluez
Author: Kamel Ghali
"""

import sys
import bluetooth
import scapy

addr = None


def rfcomm_floodingTest(addr, targetPort):
	
	print("Connecting to target on port {}".format(targetPort))
	
	# Create the client socket
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	
	try:
		sock.connect((addr, targetPort))
	except:
		print("Connection failed. Is the target device on?")
		sys.exit(0)
	
	"""
	The following lines contain the actual execution of the flooding test. To change the payload,
	change the value of the "data" variable to whatever you like. By default it's just a bunch of As.
	"""
	data = "////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////"
	print("Connection to target complete.\nPress Enter to begin flooding of RFCOMM data. Press Ctrl + C to end the test or let it end on its own.")
	
	
	#If the test ends on its own, it probably means that the target ended the connection or its Bluetooth stack crashed.
	#TODO: Add functionality to gracefully recover from errors caused by forced disconnection or target device crash/lack of response/timeout
	input()
	try:
		while True:
			sock.send(data)
			print("Sending payload: {}".format(data))
	
	except (KeyboardInterrupt):
		print("\n \nTest interrupted by user")
		
	except bluetooth.btcommon.BluetoothError:
		#print("\n \nConnection timed out. Target device may have crashed.")
		print("\n \nBluetooth Error of some kind occurred.")
	
	except:
		print("An error occurred.")
	
	sock.close()


if len(sys.argv) == 2: #Case in which a Bluetooth Address is specified, BUT no RFCOMM Channel
	print("Bluetooth Address with no RFCOMM Channel specified. Initiating SDP scan for RFCOMM Services.")
	addr = sys.argv[1]
	
	services = bluetooth.find_service(address=addr) #Scan target for Services
	
	numRFCOMMServices = 0
	
	if len(services) == 0:
		print("No services found")
		sys.exit(0)
		
	else:
		for svc in services:
			if svc["protocol"] == "RFCOMM": #Only test services connected to an RFCOMM channel
				targetPort = int(svc["port"])
				
				numRFCOMMServices = (numRFCOMMServices + 1)
				
				print("RFCOMM service {} found on channel {}".format(svc["name"],targetPort))
				
				rfcomm_floodingTest(addr, targetPort) #Perform the test
		
		if numRFCOMMServices == 0:
			print("No RFCOMM Services found")
			sys.exit(0)
		else:
			print("Test performed on {} RFCOMM Channels".format(numRFCOMMServices))
			print("Thank you for using RFCOMMrade!")
			sys.exit(0)
	

elif len(sys.argv) == 3: #Case when both a Bluetooth Address AND RFCOMM Channel are specified
	addr = sys.argv[1]
	targetPort = int(sys.argv[2])
	print("Bluetooth Address and RFCOMM Channel specified. Initiating flooding test on {} on RFCOMM Channel {}".format(addr, targetPort))
	
	rfcomm_floodingTest(addr, targetPort)
	
	print("Thank you for using RFCOMMrade!")
	sys.exit(0)


else:
	print("Usage: 'python3 rfcommrade <bt address> <RFCOMM Channel Number>'\n<bt_address> format is 12:34:56:AB:CD:EF")
	sys.exit(0)
	



