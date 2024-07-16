from flask import (
    Flask,
    jsonify,
    request,
    abort
)

from datetime import datetime

class CuentaUsuario:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos

    def __str__(self):
        return f'Cuenta: Numero: {self.numero}, nombre: {self.nombre}, saldo: {self.saldo}, contactos: {self.contactos})'

    def format(self):
        return {
            'numero': self.numero,
            'saldo': self.saldo
        }

    def contactosFormato(self):
        cont = {}
        for i in self.contactos:
            contact = CuentaUsuario.get_cuentaPorNombre(i)
            cont[contact.numero] = i
        return cont
    
    def historial(self):
        #operaciones
        pagos = []
        recibidos = []
        for operacion in operaciones:
            if operacion.origen == self.numero:
                pagos.append(operacion)
            elif operacion.destino == self.numero:
                recibidos.append(operacion)
        return pagos, recibidos
    
    def saldoActualizar(self, valor):
        self.saldo += valor

    def pagar(self, destino, valor, emisor, receptor):
        if self.saldo >= valor:
            return False
        
        fechaHoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        operaciones.append(Operacion(emisor, destino, valor, fechaHoy))
        self.saldoActualizar(-valor)
        cuentas[emisor] = CuentaUsuario(self.numero, self.nombre, self.saldo, self.contactos)
        destino.saldoActualizar(valor)
        cuentas[receptor] = destino

        return fechaHoy
    
    @staticmethod
    def cuentaPorNumero(numero):
        for cuenta in range(len(cuentas)):
            if cuentas[cuenta].numero == numero:
                return cuentas[cuenta], cuenta
        return -1, -1
    
    @staticmethod
    def cuentaPorNombre(nombre):
        for cuenta in cuentas:
            if cuenta.nombre == nombre:
                return cuenta
        return -1
    
    @staticmethod
    def nombrePorNumero(numero):
        for cuenta in cuentas:
            if cuenta.numero == numero:
                return cuenta.nombre
        return -1

    @staticmethod
    def datosCuenta(datos):
        cuentas = datos  


class Operacion:
    def __init__(self, origen, destino, valor, fecha):
        self.destino = destino
        self.origen = origen
        self.valor = valor
        self.fecha = fecha
        
    def __reporte__(self):
        return f'Operacion: Destino = {self.destino}, Origen = {self.origen}, Valor = {self.valor}, Fecha = {self.fecha}'       

    def OperacionRealizado(self):
        nombre = CuentaUsuario.cuentaPorNombre(self.destino)
        return f'Pago realizado de {self.valor} a {nombre}'

    def OperacionRecibido(self):
        nombre = CuentaUsuario.cuentaPorNombre(self.destino)
        return f'Pago recibido de {self.valor} de {nombre}'


#Data inicial 
cuentas = [
    CuentaUsuario("21345", "Arnaldo", 200, ["123", "456"]),
    CuentaUsuario("123", "Luisa", 400, ["456"]),
    CuentaUsuario("456", "Andrea", 300, ["21345"])
]

operaciones = []

app = Flask(__name__)

@app.route('/', methods=['GET'])
def OtenerContactos():
    return jsonify({
        'succes': True,
    })

@app.route('/billetera/contactos')
def contactos():
    error_404 = False
    error_422 = False
    try:
        numero = request.args.get('minumero')
        if numero == "" or numero is None:
            error_422 = True
            abort(422)
        
        c, i = CuentaUsuario.cuentaPorNumero(numero)

        if c == -1:
            error_404 = True
            abort(404)

        return jsonify({
            'success': True,
            'contactos': c.contactosFormato()
        })
    except Exception as e:
        print(e)
        if error_404:
            abort(404)
        elif error_422:
            abort(422)
        else:
            abort(500)

@app.route('/billetera/pagar')
def Pagar():
    error404 = False
    error422 = False
    error406 = False
    try:
        numero = request.args.get('minumero')
        numeroDestino = request.args.get('numerodestino')
        valor = request.args.get('valor')

        if (numero == None or numero is None) or (numeroDestino == "" or numeroDestino is None):
            error422 = True
            abort(422)

        if numero == numeroDestino:
            error406 = True
            abort(406)
        
        if valor == "" or valor == None:
            error422 = True
            abort(422)
        try:
            valor = float(valor)
        except Exception as e1:
            print(e1)
            error406 = True
            abort(406)
        
        if valor <= 0:
            error406 = True
            abort(406)
            
        emisor, i = CuentaUsuario.cuentaPorNumero(numero)
        receptor, j = CuentaUsuario.cuentaPorNumero(numeroDestino)
        
        if emisor == -1 or receptor == -1:
            error404 = True
            abort(404)
        
        operacion = emisor.pagar(receptor, valor, i, j)
        if operacion == -1:
            error406 = True
            abort(406)
        
        return jsonify({
            'success': True,
            'fecha': f'Realizado en {operacion}'
        })
        
    except Exception as e:
        print(e)
        if error404:
            abort(404)
        elif error422:
            abort(422)
        elif error406:
            abort(406)
        else:
            abort(500)
            
        

@app.route('/billetera/historial')
def OtenerHistorial():
    #aqui manejamos errores conocidos
    error404 = False
    error422 = False
    try:
        numero = request.args.get('minumero')
        if numero == None:
            error404 = True
            abort(404)
        
        cuenta, index = CuentaUsuario.cuentaPorNumero(numero)
        
        if cuenta == -1:
            error404 = True
            abort(404)
        
        pagos, recibidos = cuenta.historial()
        pagos = [p.format_p() for p in pagos]
        recibidos = [r.format_p() for r in recibidos]

        return jsonify({
            'success': True,
            'datos': cuenta.format(),
            'pagos': pagos,
            'recibidos': recibidos
        })

    except Exception as e:
        print(e)
        if error404:
            abort(404)
        elif error422:
            abort(422)
        else:
            abort(500)

#aqui manejamos errores conocidos, previamente mencionados
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not found'
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
    }), 422

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

@app.errorhandler(406)
def not_acceptable(error):
    return jsonify({
        'success': False,
        'error': 406,
        'message': 'Not Acceptable'
    }), 406


if __name__ == '__main__':
    app.run(debug=True)


























