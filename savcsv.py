#!/usr/bin/env python3
# '-*- coding: utf-8 -*-'

'''

    sauvegarde des donnees envoyées par la liaison serie dans un fichier csv
    

    ****        historique      ****
    * 	0.0.1 	creation du programme, lecture de trames et enregistrement

 '''

import serial
import sys
import datetime


port = '/dev/ttyUSB0'
baud = '19200'
datadir = './data'

def mkdir_p(repertoire):

	try:
		folder=os.path.dirname(repertoire)  
		if not os.path.exists(folder):  
			os.makedirs(folder)
		return True
	except:
		return False

    
if __name__=='__main__':
##    print ("Found ports:")
##    for n,s in scan():
##        print ("(%d) %s" % (n,s))
##    selection = input("Enter port number:")

#	print "repertoire de donnees :%s" % (os.path.dirname(datadir))
#	if (mkdir_p(datadir)):
#		print "Created dir :%s" % (os.path.dirname(datadir))

	filename = datadir + '/' + str(datetime.datetime.now() ).split('.')[0] + '.csv'
	print filename
	try:
##        ser = serial.Serial(eval(selection), 9600, timeout=1)
		ser = serial.Serial(port, baud, timeout=1)
		print("connected to: " + ser.portstr)
	except serial.SerialException:
		pass
	while True:
		# Read a line and convert it from b'xxx\r\n' to xxx
		line = ser.readline()
		if line:  # If it isn't a blank line
			f = open(filename, 'a')	
			f.write(line)
			f.close()
			print line
			#sys.stdout.write(line) # pas \n en plus de line
ser.close()
