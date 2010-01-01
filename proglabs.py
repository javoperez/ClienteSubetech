import httplib
import urllib

y= None
while y!= "exit":
	print "Ingresa <exit> para salir" 
	y= raw_input("Esperando codigo... ")

	try:
		
		params = urllib.urlencode({'clave': y})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("subetech.proglabs.co:49195")
		conn.request("POST", "/descontar/", params, headers)
		response = conn.getresponse()
		print response.status, response.reason
		data = response.read()
		conn.close()
		result = ""
	except:
		import sys
		print sys.exc_info()[:2]
