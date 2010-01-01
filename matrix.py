#!/usr/bin/env python
# coding=utf-8

import httplib
import urllib
import cordenadas
import time
import multiprocessing
#####DECOMENTAR LA SIGUIENTE:
#import gpio

cmd= ""
Latitud=""
Longitud=""
y= None

def leer():
	f = open("lat_long.txt")
	lectura=f.read()
	f.close()
	letra=""
	for letra in lectura:
		Latitud= Latitud+letra
		if letra== ",":
			break

	Longitud= lectura.replace(Latitud, "")
	Latitud=Latitud.replace(",", "")

	if Latitud== "nan":
		Latitud= "18.8091843"
	if Longitud== "nan":
		Longitud= "-99.2206003"
	print "Latitud", Latitud
	print "Longitud", Longitud
	global Latitud
	global Longitud

def conectar():
	try:

		params = urllib.urlencode({'clave': cmd,  'longitud':Longitud, 'latitud':Latitud})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("localhost:8000")
		conn.request("POST", "/descontar/", params, headers)
		response = conn.getresponse()
		#print response.status, response.reason
		data = response.read()
		conn.close()
		result = ""
		
	except:
		import sys
		print sys.exc_info()[:2]
		return 401
	return response.status
	

# SOLO PARA PRUEBAS... deberá BORRARSE

def leerA():
	a_r=""
	f = open("AB.txt")
	lectura=f.read()
	f.close()
	letra=""
	for letra in lectura:
		a_r= a_r+letra
		if letra== ",":
			break
	a_r=a_r.replace(",", "")
	if a_r=="True":
		a_r=True
	if a_r=="False":
		a_r=False
	return a_r

def leerB(arg):
	f = open("AB.txt")
	lectura=f.read()
	f.close()
	letra=""
	arg=str(arg)
	b_r= lectura.replace(arg+",", "")
	if b_r=="True":
		b_r=True
	if b_r=="False":
		b_r=False

	return b_r

def detectarpcduino(estado_queue, permiso_queue):
	SensorA = "gpio4"
	SensorB = "gpio5"
	print "Detectando"
	## ESTO DEBE DESCOMENTARSE
	"""estado= None
							z= None
							while 1:
								A= gpio.digitalRead(sensorA)
								B= gpio.digitalRead(sensorB)
						
								if A==True:
									estado= "entra"
									## RECUERDA HACER GLOBAL EL estado
									estado_queue.put("entra")
									while B==False and y!= "salir":
										B=gpio.digitalRead(sensorB)
										if B==True:
											A=False
											while B==True:
												B=gpio.digitalRead(sensorB)
											z= "salir"
						
								z=None
										
								if B==True:
										estado= "sale"
										while A==False and y!= "salir":
											A=gpio.digitalRead(sensorA)
											if A==True:
												B=False
												while A==True:
													A=gpio.digitalRead(sensorA)
												z= "salir"
								if estado!="None":
									print estado
								"""
	### ESTO ES TEMPORAL (DEBES BORRAR)
	estado= None
	estado_queue.put(None)
	z= None
	while 1:
		A= leerA()
		B= leerB(A)

		if A==True:
			estado= "entra"
			estado_queue.put("entra")
			while B==False and y!= "salir":
				B=leerB(A)
				if B==True:
					A=False
					while B==True:
						B=leerB(A)
					z= "salir"

		z=None
				
		if B==True:
				estado= "sale"
				estado_queue.put("sale")
				while A==False and y!= "salir":
					A=leerA()
					if A==True:
						B=False
						while A==True:
							A=leerA()
						z= "salir"
		print estado
		estado= None
		time.sleep(1)

def decidir(estado_queue, permiso_queue):
	### DESCOMENTAR EN PCDUINO
	"""	rojo = "gpio6"
	verde = "gpio7"
	alarma= "gpio8"
	gpio.pinMode(rojo, gpio.OUTPUT)
	gpio.pinMode(verde, gpio.OUTPUT)
	gpio.pinMode(alarma, gpio.OUTPUT)"""
	while 1:
		edo= estado_queue.get()
		if edo== None or edo== "sale":
			edo= False
		if edo=="entra":
			edo= True
		print "entre y el valor es: ", edo
		perm= permiso_queue.get()
		print "e lpermiso es: ", perm

		if edo==False and perm== False:
			# gpio.digitalWrite(alarma, gpio.LOW)
			# gpio.digitalWrite(rojo, gpio.LOW)
			# gpio.digitalWrite(verde, gpio.LOW)
			print "alarma, rojo y verde apagados"
		if edo==False and perm== True:
			#gpio.digitalWrite(verde, gpio.HIGH)
			"verde prendido"
		if edo==True and perm== False:

			# gpio.digitalWrite(alarma, gpio.HIGH)
			# gpio.digitalWrite(rojo, gpio.HIGH)
			print "Rojo y alarma prendidos.. delay"
			time.sleep(3)
			# estado_queue.put(False)
			# permiso_queue.put(False)

		if edo==True and perm== True:
			time.sleep(.2)
			estado_queue.put(None)
			permiso_queue.put(False)			

def main():

	print "Creando procesos de comunicación..."
	estado_queue =multiprocessing.Queue()
	permiso_queue =multiprocessing.Queue()
	t = multiprocessing.Process(target=detectarpcduino, args=(estado_queue,permiso_queue))
	t2 = multiprocessing.Process(target=decidir, args=(estado_queue,permiso_queue))

	t.daemon = True
	t2.daemon = True
	try:
		t.start()
		time.sleep(.1)
		t2.start()
		time.sleep(.1)
		
	except:
		print "ERROR: No se pudieron crear los procesos de comunicación."


	while(cmd != "exit"):
		print "Ingresa <exit> para salir " 
		cmd = raw_input("Esperando codigo... ")
		global cmd
		leer()
		permiso= conectar()
		print "permiso: "

		if permiso==200:
			permiso_queue.put(True)
		else:
			permiso_queue.put(False)
		print permiso_queue.get()

		Latitud=""
		Longitud=""
		global Latitud
		global Longitud

	print "Terminando procesos..."
	t.terminate()
	print t

if __name__ == "__main__":
	main()
