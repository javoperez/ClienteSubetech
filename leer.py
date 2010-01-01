

def leer():
	f = open("lat_long.txt")
	lectura=f.read()
	f.close()

	Latitud=""
	letra=""
	for letra in lectura:
		Latitud= Latitud+letra
		if letra== ",":
			break

	Longitud= lectura.replace(Latitud, "")
	Latitud=Latitud.replace(",", "")

	if Latitud== "nan":
		Latitud= 0
	if Longitud== "nan":
		Longitud= 0
	print "Latitud", Latitud
	print "Longitud", Longitud

	



