#! /usr/bin/python
#-*- encoding: -utf-8-*-

import os
from gps import *
from time import *
import time
import threading

gpsd = None #variable global
 
os.system('clear') #borra el contenido de la terminal

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #poner disponible la variable gpsd
    gpsd = gps(mode=WATCH_ENABLE) #comienza a buscar info
    self.current_value = None
    self.running = True #El "Thread" se pone en corrida
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #toma la informacion del gpsd hasta que se vacía el buffer
Coordenadas= "Entre"
if __name__ == '__main__':
  gpsp = GpsPoller() # comienza el thread
  try:
    
    gpsp.start() # comienza la lectura
    while True:
      #Tarda unos segundos en tomar buena información

      os.system('clear')
      f=open("lat_long.txt","w")
      print
      print ' Lectura GPS'
      print '----------------------------------------'
      f.write(Coordenadas)
     # f.write("longitud: ",gpsd.fix.longitud, "\n")
      print 'latitud    ' , gpsd.fix.latitude
      print 'longitud   ' , gpsd.fix.longitude
      print 'speed (m/s) ' , gpsd.fix.speed
      Coordenadas= str(gpsd.fix.latitude)+","+ str(gpsd.fix.longitude)
      f.close()

      time.sleep(5) #delay
 
  except (KeyboardInterrupt, SystemExit): #si precionas ctrl+c
    print "\nMatando el Thread..."
    gpsp.running = False
    gpsp.join() # Espera a que el thread termine
    #Cierra el archivo
  print "Listo \nsaliendo..."