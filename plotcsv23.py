#!/usr/bin/env python3
# '-*- coding: utf-8 -*-'

'''

    affichage graphique du fichier passé en parametre fichier csv
    

    ****        historique      ****
    * 	0.0.1 	creation du programme, lecture de trames et enregistrement

 '''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import io
import numpy as np
import datetime as dt
from datetime import datetime
import matplotlib.dates as mdates
import sys


#datadir = './data/'
titre = ''
filename = ''

fig = plt.figure()
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2)
ax3 = fig.add_subplot(3,1,3)
fig = plt.gcf()
fig.autofmt_xdate()

def animate(i):
	pullData = open(filename,"r").read()
#	data = np.genfromtxt(io.BytesIO(pullData), unpack=True, dtype=None,
#			names = ['day', 'tension', 'Inst' , 'courant', 'ia_MoyGlHeure', 'ia_Cumulgl', 'ia_Cumul', 'ia_Cumult'],
#			delimiter = ',', converters={0: lambda x: datetime.strptime(x, '%Y/%m/%d %H:%M:%S')})
	data = np.genfromtxt(io.BytesIO(pullData.encode('utf-8')), unpack=True, dtype=None,
			names = ['day', 'tension', 'Inst' , 'courant', 'ia_MoyGlHeure', 'ia_Cumulgl', 'ia_Cumul', 'ia_Cumult'],
			delimiter = ',', converters={0: lambda x: datetime.strptime(x.decode("utf-8"), '%Y/%m/%d %H:%M:%S')})
	x = data['day']
	y = data['tension']
	v = data['courant']
	z = data['ia_MoyGlHeure']
	u = data['ia_Cumulgl']
	t = data['ia_Cumul']
	w = data['ia_Cumult']

	#ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	#ax1.clear()

#b: blue
#g: green
#r: red
#c: cyan
#m: magenta
#y: yellow
#k: black
#w: white

	fig.suptitle( titre )
	leg1, = ax1.plot(x, y, color='b', label='V')
	leg2, = ax2.plot(x, v, color='k', label='I')
	leg3, = ax2.plot(x, z, color='g', label='Igl')
	leg4, = ax3.plot(x, u, color='r', label='Cumulgl')
	leg5, = ax3.plot(x, t, color='c', label='Cumul')
	leg6, = ax3.plot(x, w, color='m', label='Cumult')
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
	lbl1 = [leg1]
	lbl2 = [leg2, leg3]
	lbl3 = [leg4, leg5, leg6]
	ax1.legend(lbl1, [lbl1_.get_label() for lbl1_ in lbl1], loc= 'best', fontsize= 'small')
	ax2.legend(lbl2, [lbl2_.get_label() for lbl2_ in lbl2], loc= 'best', fontsize= 'small')
	ax3.legend(lbl3, [lbl3_.get_label() for lbl3_ in lbl3], loc= 'best', fontsize= 'small')


	plt.xticks(rotation=60)
if __name__=='__main__':
	# expects 1 arg - serial port string
	if(len(sys.argv) != 2):
		print ('Example usage: python plotcsv2.py 2017-12-12\ 08:15:00.csv')
		exit(1)
	filename = sys.argv[1];
	#filename = 'data/2017-12-15 17:47:28.csv'
	ani = animation.FuncAnimation(fig, animate, interval=1000)
	f = open(filename, 'r')
	line = f.readline()
	f.close()
	line = line.split(',')
	if titre == '':
		titre = 'Etat de batterie du campingcar au : ' + line[0]
	plt.show()
