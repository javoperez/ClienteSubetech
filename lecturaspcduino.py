#!/usr/bin/env python
# coding=utf-8
import time

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
	print a_r
	return a_r

def leerB(arg):
	f = open("AB.txt")
	lectura=f.read()
	f.close()
	letra=""
	b_r= lectura.replace(arg+", ", "")
	print b_r
	return b_r

while 1:
	A= leerA()
	B= leerB(A)
	time.sleep(.5)
