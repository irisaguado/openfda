import http.server
import http.client
import socketserver
import json

PORT = 8000
formulario = "formularioprueba.html"
socketserver.TCPServer.allow_reuse_address = True

nombre_servidor = "api.fda.gov"
parametro_busqueda = "/drug/label.json"
headers = {'User-Agent': 'http-client'}


class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def formulario(self):
        with open(formulario, "r") as f:
            formulario_r = f.read()
        return formulario_r

    def openfda(self, limit=1, parametro=""):
        """Realizar una peticion a openFPGA"""

        peticion = "{}?limit={}".format(parametro_busqueda, limit)

        if parametro != "":
            peticion += "&{}".format(parametro)

        print("Recurso solicitado: {}".format(peticion))

        conexion = http.client.HTTPSConnection(nombre_servidor)

        conexion.request("GET", peticion, None, headers)

        respuesta = conexion.getresponse()

        if respuesta.status == 404:
           print("ERROR. Recurso {} no encontrado".format(parametro_busqueda))
           exit(1)



        respuesta_json = respuesta.read().decode("utf-8")
        conexion.close()

        return json.loads(respuesta_json)


    def principio_activo(self, limit, parametro):
        respuestas = self.openfda(limit, parametro)

        meta = respuestas['meta']

        total = meta['results']['total']
        limit = meta['results']['limit']

        mensaje = ('''
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <p>Nombre genérico</p>
        <ul>''')
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['generic_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li>{}</li>\n".format(nombre)

        mensaje += ('''
        </ul>
        <a href="/">Formulario</a>
    </body
</html>''')
        return mensaje

    def lista_drug(self, limit):
        respuestas = self.openfda(limit)

        mensaje = ('''
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <p>Nombre genérico</p>
        <ul>''')
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['generic_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li>{}</li>\n".format(nombre)

        mensaje += ('''
        </ul>
        <a href="/">Formulario</a>
    </body
</html>''')
        return mensaje

    def lista_empresas(self, limit):
        respuestas = self.openfda(limit)

        mensaje = ('''
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <p>Empresas</p>
        <ul>''')
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['manufacturer_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li>{}</li>\n".format(nombre)

        mensaje += ('''
        </ul>
        <a href="/">Formulario</a>
    </body
</html>''')
        return mensaje

    def buscar_company(self, limit, parametro):
        respuestas = self.openfda(limit, parametro)

        meta = respuestas['meta']

        total = meta['results']['total']
        limit = meta['results']['limit']

        mensaje = ('''
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <p>Nombre genérico</p>
        <ul>''')
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['generic_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li>{}</li>\n".format(nombre)

        mensaje += ('''
        </ul>
        <a href="/">Formulario</a>
    </body
</html>''')
        return mensaje

    def list_warnings(self, limit):
        respuestas = self.openfda(limit)

        mensaje = ('''
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <p>Advertencias</p>
        <ul>''')
        for resp in respuestas['results']:

            if 'warnings' in resp:
                advertencia = resp['warnings'][0]

            else:
                advertencia = "Desconocido"

            mensaje += "<li>{}</li>\n".format(advertencia)

        mensaje += ('''
        </ul>
        <a href="/">Formulario</a>
    </body
</html>''')
        return mensaje

    def do_GET(self):
        print("Recurso pedido: {}".format(self.path))

        mensaje = ""

        if self.path == "/":
            mensaje = self.formulario()

        else:
            datos_form = self.path.split("?")
            recursos = datos_form[0]
            recurso = recursos.strip('/')
            print(recurso)
            parametros = datos_form[1]


            if parametros.find('&') != -1:
                param = parametros.split('&')
                for dato in param:
                    datos_param = dato.split('=')
                    if datos_param[0] == 'limit':
                        limit = datos_param[1]
                    elif datos_param[0] == 'company':
                        parametro = 'search=openfda.manufacturer_name:'+'"'+datos_param[1]+'"'
                    elif datos_param[0] == 'active_ingredient':
                        parametro = 'search=active_ingredient:'+'"'+datos_param[1]+'"'


            else:
                datos_param = parametros.split("=")
                limit = datos_param[1]


            if recurso == "listDrugs":
                mensaje = self.lista_drug(limit)

            elif recurso == "searchDrug":
                mensaje = self.principio_activo(limit, parametro)

            elif recurso == "listCompanies":
                mensaje = self.lista_empresas(limit)

            elif recurso =="searchCompany":
                mensaje = self.buscar_company(limit, parametro)

            elif recurso =="listWarnings":
                mensaje = self.list_warnings(limit)



        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(mensaje, "utf8"))
        return

Handler = TestHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving at port", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
