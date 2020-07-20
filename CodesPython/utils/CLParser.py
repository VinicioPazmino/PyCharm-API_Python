import sys

def CLParser(args):
	try:
		iip = args.index('-ip')
		ipAddress = args[iip+1]
	except ValueError:
		ipAddress = "150.244.57.171"
		print("No IP Address provided, trying using default 150.244.57.171")
	try:
		iport = args.index('-port')
		port = int(args[iport+1])
	except ValueError:
		port = 8889
		print("No Port provided, trying using default 8889")
	try:
		ipath = args.index('-cfgpath')
		cfgpath = args[ipath+1]
	except ValueError:
		cfgpath = "./config.ini"
		print("No path to the config file provided, trying using default ./config.ini")
	return ipAddress, port, cfgpath
