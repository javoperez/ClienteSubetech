#!/usr/bin/env python
# coding=utf-8

import time
import multiprocessing
import gpio

y=None
sensor1 = "gpio5"
sensor2="gpio4"


def detectarpcduino(estado_queue, permiso_queue):
	estado= None
	while 1:
		A=gpio.digitalRead(sensor1)
		B= gpio.digitalRead(sensor2)

		if A==True:
			estado= "entra"
			while B==False and y!= "salir":
				#print "ciclo 1"
				B=gpio.digitalRead(sensor2)
				if B==True:
					A=False 
					while B==True:
						B=gpio.digitalRead(sensor2)
						#print "Ciclo 2"
					y= "salir"

		y=None
			
		if B==True:
				estado= "sale"
				while A==False  and y!= "salir":
					#print "ciclo 1"
					A=gpio.digitalRead(sensor1)
					if A==True:
						B=False 
						while A==True:
							A=gpio.digitalRead(sensor1)
							#Sprint "Ciclo 2"
						y= "salir"
		
		if estado=='sale' or estado== 'entra':
			print estado
			time.sleep(1)
			
		estado= None


def main():
	print "Creando procesos de comunicación..."
	estado_queue =multiprocessing.Queue()
	permiso_queue =multiprocessing.Queue()
	t = multiprocessing.Process(target=detectarpcduino, args=(estado_queue,permiso_queue))
	t.daemon = True

	try:
		t.start()
		time.sleep(100)
	except:
		print "ERROR: No se pudieron crear los procesos de comunicación."



if __name__ == "__main__":
	main()