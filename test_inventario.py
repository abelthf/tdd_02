import pytest

from inventario import InvalidQuantityException
from inventario import Inventario
from inventario import NoSpaceException
from inventario import ItemNotFoundException


def test_compra_y_venta_nikes_adidas():
    # Creaci√≥n de objeto inventario
    inventario = Inventario()
    assert inventario.limite == 100
    assert inventario.total_items == 0

    # A√±ade las sapatillas neuvas Nike
    inventario.add_nuevo_stock("Zapatillas Nike", 50.00, 10)
    assert inventario.total_items == 10

    # Agrega los pantalones nuevos de Chandal Adidas
    inventario.add_nuevo_stock('Pantalones Adidas', 70.00, 5)
    assert inventario.total_items == 15

    # Retira 2 zapatillas para vender al primer cliente
    inventario.remueve_stock('Zapatillas Nike', 2)
    assert inventario.total_items == 13

    # Retira 1 pantalon de chandal para venderlo al proximo cliente
    inventario.remueve_stock('Pantalones Adidas', 1)
    assert inventario.total_items == 12


def test_inventario_default():
    """Test que tiene por defecto el limite = 100"""
    inventario = Inventario()
    assert inventario.limite == 100
    assert inventario.total_items == 0


def test_limite_inventario_personalizado():
    """Test que tiene un limite personalizado"""
    inventario = Inventario(limite=25)
    assert inventario.limite == 25
    assert inventario.total_items == 0
    return Inventario(10)


@pytest.fixture
def no_stock_inventario():
    """Retorna un inventario vacio que puede almacenar 10 items"""
    return Inventario(10)


# def test_add_nuevo_stock_satisfactorio(no_stock_inventario):
#     no_stock_inventario.add_nuevo_stock('Test Casaca', 10.00, 5)
#     assert no_stock_inventario.total_items == 5
#     assert no_stock_inventario.stocks['Test Casaca']['precio'] == 10.00
#     assert no_stock_inventario.stocks['Test Casaca']['cantidad'] == 5


@pytest.mark.parametrize('nombre,precio,cantidad,exception', [
    ('Test Casaca', 10.00, 0, InvalidQuantityException(
        'No se puede agregar una cantidad de 0. Todo stock nuevo debe tener al menos 1 item'))])
def test_add_new_stock_bad_input(nombre, precio, cantidad, exception):
    inventario = Inventario(10)
    try:
        inventario.add_nuevo_stock(nombre, precio, cantidad)
    except InvalidQuantityException as inst:
        # Primero asegurese de que la excepcion sea del tipo correcto
        assert isinstance(inst, type(exception))
        # Asegurarse de que las excepciones tengan el mismo mensaje
        assert inst.args == exception.args
    else:
        pytest.fail("Error esperado pero no encontrado")


# @pytest.mark.parametrize('nombre,precio,cantidad,exception', [
#     ('Test Casaca', 10.00, 0, InvalidQuantityException(
#         'No se puede agregar una cantidad de 0. Todo stock nuevo debe tener al menos 1 item')),
#     ('Test Casaca', 10.00, 25, NoSpaceException(
#         'No se pueden agregar estos 25 items. Solo se pueden almacenar 10 items mas'))
# ])
# def test_add_new_stock_bad_input(no_stock_inventario, nombre, precio, cantidad, exception):
#     try:
#         no_stock_inventario.add_nuevo_stock(nombre, precio, cantidad)
#     except (InvalidQuantityException, NoSpaceException) as inst:
#         # Primero asegurese de que la excepcion sea del tipo correcto
#         assert isinstance(inst, type(exception))
#         # Asegurarse de que las excepciones tengan el mismo mensaje
#         assert inst.args == exception.args
#     else:
#         pytest.fail("Error esperado pero no encontrado")


@pytest.mark.parametrize('nombre,precio,cantidad,exception', [
    ('Test Casaca', 10.00, 0, InvalidQuantityException(
        'No se puede agregar una cantidad de 0. Todo stock nuevo debe tener al menos 1 item')),
    ('Test Casaca', 10.00, 25, NoSpaceException(
        'No se pueden agregar estos 25 items. Solo se pueden almacenar 10 items mas')),
    ('Test Casaca', 10.00, 5, None)
])
def test_add_nuevo_stock(no_stock_inventario, nombre, precio, cantidad, exception):
    try:
        no_stock_inventario.add_nuevo_stock(nombre, precio, cantidad)
    except (InvalidQuantityException, NoSpaceException) as inst:
        # First ensure the exception is of the right type
        assert isinstance(inst, type(exception))
        # Ensure that exceptions have the same message
        assert inst.args == exception.args
    else:
        assert no_stock_inventario.total_items == cantidad
        assert no_stock_inventario.stocks[nombre]['precio'] == precio
        assert no_stock_inventario.stocks[nombre]['cantidad'] == cantidad


# ...
# Agregue un nuevo accesorio que contenga acciones por defecto
# Esto facilita la escritura de pruebas para nuestra función de remover
@pytest.fixture
def ten_stock_inventario():
    """Devuelve un inventario con algunos artículos de stock de prueba"""
    inventario = Inventario(20)
    inventario.add_nuevo_stock('Puma Test', 100.00, 8)
    inventario.add_nuevo_stock('Reebok Test', 25.50, 2)
    return inventario

# ...
# Tenga en cuenta los parametros adicionales, necesitamos establecer nuestra 
# expectativa de que totales deberían ser despues de nuestra accion de eliminacion
@pytest.mark.parametrize('nombre,cantidad,exception,nueva_cantidad,nuevo_total', [
    ('Puma Test', 0,
     InvalidQuantityException(
         'No se puede eliminar una cantidad de 0. Debe eliminar al menos 1 item'),
        0, 0),
    ('No Aqui', 5,
     ItemNotFoundException(
         'No se puede encontrar No Aqui en nuestro stock. No se puede eliminar el stock que no existe'),
        0, 0),
    ('Puma Test', 25,
     InvalidQuantityException(
         'No se pueden eliminar estos 25 elementos. Solo hay 8 articulos en stock'),
     0, 0),
    ('Puma Test', 5, None, 3, 5)
])
def test_remueve_stock(ten_stock_inventario, nombre, cantidad, exception,
                      nueva_cantidad, nuevo_total):
    try:
        ten_stock_inventario.remueve_stock(nombre, cantidad)
    except (InvalidQuantityException, NoSpaceException, ItemNotFoundException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert ten_stock_inventario.stocks[nombre]['cantidad'] == nueva_cantidad
        assert ten_stock_inventario.total_items == nuevo_total
