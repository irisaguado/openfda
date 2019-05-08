
import http.server
import http.client
import socketserver
import json

PORT = 8000
formulario = "formulario.html"
socketserver.TCPServer.allow_reuse_address = True


class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def formulario(self):
        with open(formulario, "r") as f:
            formulario_r = f.read()
        return formulario_r


    def openfda_pet(self, limit=1, parametro=""):

        nombre_servidor = "api.fda.gov"
        parametro_busqueda = "/drug/label.json"
        headers = {'User-Agent': 'http-client'}

        peticion = "{}?limit={}".format(parametro_busqueda, limit)

        if parametro != "":
            peticion += "&{}".format(parametro)

        print("Recurso solicitado: {}".format(peticion))

        conexion = http.client.HTTPSConnection(nombre_servidor)

        conexion.request("GET", peticion, None, headers)

        respuesta = conexion.getresponse()

        if respuesta.status == 404:
           print("ERROR. Recurso {} no encontrado".format(peticion))
           exit(1)

        respuesta_json = respuesta.read().decode("utf-8")
        conexion.close()

        return json.loads(respuesta_json)


    def principio_activo(self, parametro):
        limit = 10
        respuestas = self.openfda_pet(limit, parametro)

        meta = respuestas['meta']

        total = meta['results']['total']
        limit = meta['results']['limit']

        mensaje = ("""
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style = 'background-color:rgb(241, 208, 245)'>
        <h2 style = 'color:rgb(110, 1, 110)'>Nombre genérico de los fármacos que contienen el principio activo introducido</h2>
        <ul>""")
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['generic_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li><h5 style = 'color:rgb(158, 15, 158)'>{}</h5></li>\n".format(nombre)

        mensaje += ("""
        </ul>
    </body>
</html>""")
        return mensaje

    def lista_drug(self, limit):
        respuestas = self.openfda_pet(limit)

        mensaje = ("""
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style = 'background-color:rgb(241, 208, 245)'>
        <h2 style = 'color:rgb(110, 1, 110)'>Nombre genérico de los fármacos</h2>
        <ul>""")
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['generic_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li><h5 style = 'color:rgb(158, 15, 158)'>{}</h5></li>\n".format(nombre)

        mensaje += ("""
        </ul>
    </body>
</html>""")
        return mensaje

    def lista_empresas(self, limit):
        respuestas = self.openfda_pet(limit)

        mensaje = ("""
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style = 'background-color:rgb(241, 208, 245)'>
        <h2 style = 'color:rgb(110, 1, 110)'>Nombre de las empresas</h2>
        <ul>""")
        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['manufacturer_name'][0]

            else:
                nombre = "Desconocida"

            mensaje += "<li><h5 style = 'color:rgb(158, 15, 158)'>{}</h5></li>\n".format(nombre)

        mensaje += ("""
        </ul>
    </body>
</html>""")
        return mensaje

    def buscar_company(self,parametro):
        limit = 10
        respuestas = self.openfda_pet(limit, parametro)

        meta = respuestas['meta']

        total = meta['results']['total']
        limit = meta['results']['limit']

        mensaje = ("""
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style = 'background-color:rgb(241, 208, 245)'>
        <h2 style = 'color:rgb(110, 1, 110)'>Nombre genérico de fármacos de la empresa que ha introducido</h2>
        <ul>""")

        for resp in respuestas['results']:

            if resp['openfda']:
                nombre = resp['openfda']['generic_name'][0]

            else:
                nombre = "Desconocido"

            mensaje += "<li><h5 style = 'color:rgb(158, 15, 158)'>{}</h5></li>\n".format(nombre)

        mensaje += ("""
        </ul>
    </body>
</html>""")
        return mensaje

    def list_warnings(self, limit):
        respuestas = self.openfda_pet(limit)

        mensaje = ("""
<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style = 'background-color:rgb(241, 208, 245)'>
        <h2 style = 'color:rgb(110, 1, 110)'>Advertencias</h2>
        <ul>""")
        for resp in respuestas['results']:

            if 'warnings' in resp:
                advertencia = resp['warnings'][0]

            else:
                advertencia = "Desconocida"

            mensaje += "<li><h5 style = 'color:rgb(158, 15, 158)'>{}</h5></li>\n".format(advertencia)

        mensaje += ("""
        </ul>
    </body>
</html>""")
        return mensaje

    def do_GET(self):

        mensaje = ""

        if self.path == "/":
            mensaje = self.formulario()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif "listDrugs" in self.path:
            datos_form = self.path.split("?")
            parametros = datos_form[1]
            datos_param = parametros.split("=")
            limit = datos_param[1]

            mensaje = self.lista_drug(limit)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif "searchDrug" in self.path:
            datos_form = self.path.split("?")
            parametros = datos_form[1]
            datos_param = parametros.split('=')
            parametro = 'search=active_ingredient:'+'"'+datos_param[1]+'"'

            mensaje = self.principio_activo(parametro)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif "listCompanies" in self.path:
            datos_form = self.path.split("?")
            parametros = datos_form[1]
            datos_param = parametros.split("=")
            limit = datos_param[1]

            mensaje = self.lista_empresas(limit)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif "searchCompany" in self.path:
            datos_form = self.path.split("?")
            parametros = datos_form[1]
            datos_param = parametros.split('=')
            parametro = 'search=openfda.manufacturer_name:'+'"'+datos_param[1]+'"'

            mensaje = self.buscar_company(parametro)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif "listWarnings" in self.path:
            datos_form = self.path.split("?")
            parametros = datos_form[1]
            datos_param = parametros.split("=")
            limit = datos_param[1]

            mensaje = self.list_warnings(limit)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm ="Acceso al servidor"')
            self.end_headers()

        elif 'redirect' in self.path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:' + str(PORT))
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset = utf8')
            self.end_headers()
            self.wfile.write("Recurso '{}' no encontrado".format(self.path).encode('utf8'))

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
print("Servidor parad")
