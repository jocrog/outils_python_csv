#!/usr/bin/env python3
# '-*- coding: utf-8 -*-'

'''

    envoi des donnees envoyées des donnees de fichier csv par la liaison serie
    - placer hc05-3 sur l'afficheur en lieu et place du bluetooth normal
    - connecter hc05-3 -> /dev/rfcomm0
	commande:
		python3 sendcsv.py 201807/echantillon.csv

    ****        historique      ****
    * 	0.0.1 	creation du programme, lecture de lignes et envoi sur le port serie
    *	2.0.1	creation des statistique en ligne pour afficheur-bargraphe V 8.0.0 

 '''

import serial
import sys
import time
import numpy as np
import datetime as dt
from datetime import datetime
from multiprocessing import Process

#port = '/dev/rfcomm0'
#port = '/dev/ttyUSB0'
port = '/dev/ttyACM0'
baud = '19200'
timeout = 6
datadir = './201807'

#libellé csv data
#{"date hour", "VBat", "Inst", "IBat", "Ah", "cumuliahg", "cumuliah", "cumuliaht"}
#2018/07/12 11:04:00,14414,-118,5263,5263,91738,94230,97753
# date hour	: date et heure de l enregistrement
# VBat		: tension de batterie
# Inst		: courant consommé par l'instrumentation
# IBat		: courant mesuré sur la borne de batterie
# Am		: Ampere/minute = moyenne de 10 acquisition/minute
# Ah		: Ampere/heure = moyenne glissante sur 1 h des 60 Am calculée toutes les minutes
# cumuliahg	: cumul Ah moyenne glissante plafonné à 100Ah
# cumuliah	: cumul Am plafonné à 100Ah
# cumuliaht	: cumul Am non plafonné

class SendClass():
	def send_data(self, ser):
		#ser.write(bytes('hello world'.encode()))
		#ser.write(b"hello world")
		#ser.write(str.encode("hello world\n"))
		while 1:
			f = open(filename, 'r')
			#this will store the line
			iline = []
			t0 = time.time()
			while 1:
				if (time.time() - t0) > timeout:
					line = f.readline() #.rstrip()
					#line = line + "," + ",".join(str(e) for e in ah) 
					#line = line + "," + ",".join(str(e) for e in cj)
					if not line:
						break
					#ser.write(line.encode('ascii'))
					ser.write(line.encode())
					print(line)
					if (ser.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
						iline = ser.read(ser.inWaiting()).decode('utf-8', errors='ignore') #read the bytes and convert from binary array to ASCII
						print(iline, end='\r') #print the incoming string without putting a new-line ('\n') automatically after every print()
						#print (iline) #print the incoming string without putting a new-line ('\n') automatically after every print()
					#time.sleep(timeout)
					t0 = time.time()
			f.close()

if __name__=='__main__':
	# expects 1 arg - serial port string
	if(len(sys.argv) != 3):
		print('Example usage: python3 sendcsv.py /dev/ttyUSB1 2017-12-12\ 08:15:00.csv')
		exit(1)
	port = sys.argv[1];
	filename = sys.argv[2];
	ah = [1, 2, 4, 8, 12, 14, 15, 14, 12, 8, 4, 2, 1, 2, 3, 4, 5, 6, 7, 8]
	#print(",".join(str(e) for e in ah))
	cj = [2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
	#print(",".join(str(e) for e in cj))
	#filename = '201807/20180705.CSV'
	#filename = '01807/echantillon.csv''
	ser = serial.Serial(port, baud)

	CT=SendClass()
	task1 = Process(target=CT.send_data, args=[ser])
	task1.start()
	# input from keybord
	commande=""
	while 1:
		commande=input().rstrip()
		if commande == "exit":
			task1.terminate()
			break
		elif commande == "start":
			if task1.is_alive() == False:
				task1.start()
		elif commande == "stop":
			if task1.is_alive():
				task1.terminate()
		else:
			commande += '\n'
			ser.write(commande.encode())
	ser.close()


