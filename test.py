import pytest
from app import app

@pytest.fixture
def Cliente():
    app.config['TESTING'] = True

    with app.test_client() as Cliente:
        yield Cliente

#Caso de prueba: El pago o la trasnferencia se realizo con exito
def testPagoExitoso(Cliente):
    response = Cliente.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=100')
    assert response.status_code == 200
    assert response.get_json().get('success') == True

#Caso de prueba: El pago no se realizo con exito ya que numero de origen y destino son iguales
def testPagoFallo(Cliente):
    response = Cliente.get('/billetera/pagar?minumero=123456789&numerodestino=123456789&valor=100')
    assert response.status_code == 406

#Caso de prueba: El contacto no se obtuvo con exito, no se ingreso el num de contacto
def testContactosFallo(Cliente):
    response = Cliente.get('/billetera/contactos')
    assert response.status_code == 422

#Caso de prueba: El pago no se obtuvo con exito, no se ingreso el num de destinatario
def testPagoFallo422(Cliente):
    response = Cliente.get('/billetera/pagar?minumero=')
    assert response.status_code == 422

#Caso de prueba: El historial se obtuvo con exito
def testHistorialExitoso(Cliente):
    response = Cliente.get('/billetera/historial?minumero=123')
    assert response.status_code == 200
    assert 'datos' in response.get_json()




