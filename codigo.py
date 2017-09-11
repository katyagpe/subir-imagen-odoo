#import win32com.client
import xmlrpclib
#import pyodbc
import base64
import csv
import os.path
import os

#server = "spectra.4toangulogestionintegral.com:8069"
server = "demos.4toangulogestionintegral.com"
database = "Surtimex-Sept"
PORT=80
user = "katya.salas@4toangulo.com"
password = '8+qnDM!;tN"6K7H'
url ='http://%s:%d/xmlrpc/' % (server,PORT)

common = xmlrpclib.ServerProxy(url+'common')
uid = common.login(database,user,password)
OdooApi = xmlrpclib.ServerProxy(url+'object')
OdooApi.timeout = 1500



ruta="/home/katya/Descargas/SUTIMEX/IMAGENES/IMAGENES/austromex"


# primer for que hace la busque en la ruta del directorio con la extencion dada
for root, dirs, files in os.walk(ruta):
    for filename in files:
    	if filename.endswith(".png") or filename.endswith(".jpg"): 

            nombre = os.path.basename(filename)
            
            nombre_solo = os.path.splitext(nombre)[0]

            filter = [[['default_code', '=', nombre_solo]]]

            print 'Imagen - ' + str(nombre_solo)
            file = open(nombre, 'rb')
            file_content = file.read()
            Imagen64 = base64.encodestring(file_content)
            #print str(Imagen64)

            
            product_id_print = OdooApi.execute_kw(database, uid, password,
            'product.product', 'search_read', filter, {'fields': ['product_id','name']})
            print 'Query exitoso - productID: '+ str(product_id_print)

            print 'Se guardara el siguiente ID - ' + str(product_id_print[0])
            product_id = OdooApi.execute_kw(database, uid, password,
	        'product.product', 'write', [[product_id_print[0]['id']],{'image' : Imagen64}])