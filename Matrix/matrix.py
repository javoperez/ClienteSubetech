#!/usr/bin/env python
# coding=utf-8

import httplib
import urllib
import time
import multiprocessing
import gpio

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
		conn = httplib.HTTPConnection("162.243.55.207:49311")
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

sensor1 = "gpio5"
sensor2="gpio4"
y=None
def detectarpcduino(estado_queue, permiso_queue):
	estado_queue.put(None)
	while 1:
		print "pase"
		A=gpio.digitalRead(sensor1)
		B= gpio.digitalRead(sensor2)

		if A==True:
			while B==False and y!= "salir":
				#print "ciclo 1"
				B=gpio.digitalRead(sensor2)
				if B==True:
					A=False 
					while B==True:
						B=gpio.digitalRead(sensor2)
						#print "Ciclo 2"
					y= "salir"
			estado_queue.put("entra")

		y=None
			
		if B==True:
				
				while A==False  and y!= "salir":
					#print "ciclo 1"
					A=gpio.digitalRead(sensor1)
					if A==True:
						B=False 
						while A==True:
							A=gpio.digitalRead(sensor1)
							#Sprint "Ciclo 2"
						y= "salir"
				estado_queue.put("sale")

		print estado_queue.get()
		if estado_queue.get()=='sale' or estado_queue.get()== 'entra':
			print estado_queue.get()
			time.sleep(.1)
		
##PRUEBA

def decidir(estado_queue, permiso_queue):
	### DESCOMENTAR EN PCDUINO
	rojo = "gpio6"
	verde = "gpio7"
	alarma= "gpio9"
	gpio.pinMode(rojo, gpio.OUTPUT)
	gpio.pinMode(verde, gpio.OUTPUT)
	gpio.pinMode(alarma, gpio.OUTPUT)
	while 1:

		edo= estado_queue.get()
		if edo== None or edo== "sale":
			edo= False
		if edo=="entra":
			edo= True
		perm= permiso_queue.get()
		print "Estado:  ", edo
		print "Permiso: ", perm
	
		if edo==False and perm== False:
			gpio.digitalWrite(alarma, gpio.LOW)
			gpio.digitalWrite(rojo, gpio.LOW)
			gpio.digitalWrite(verde, gpio.LOW)
			print "alarma, rojo y verde apagados"
		if edo==False and perm== True:
			gpio.digitalWrite(verde, gpio.HIGH)
			print "verde prendido"
		if edo==True and perm== False:

			gpio.digitalWrite(alarma, gpio.HIGH)
			gpio.digitalWrite(rojo, gpio.HIGH)
			print "Rojo y alarma prendidos.. delay"
			time.sleep(3)
			estado_queue.put(False)
			permiso_queue.put(False)

		if edo==True and perm== True:
			time.sleep(.2)
			estado_queue.put("sale")
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
