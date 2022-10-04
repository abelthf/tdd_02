class NoSpaceException(Exception):
    pass


class InvalidQuantityException(Exception):
    pass


class ItemNotFoundException(Exception):
    pass

class Inventario:
    def __init__(self, limite=100):
        self.limite = limite
        self.total_items = 0
        self.stocks = {}

    def add_nuevo_stock(self, nombre, precio, cantidad):
        if cantidad <= 0:
            raise InvalidQuantityException(
                "No se puede agregar una cantidad de {}. Todo stock nuevo debe tener al menos 1 item".format(
                    cantidad
                )
            )

        if self.total_items + cantidad > self.limite:
            remaining_space = self.limite - self.total_items
            raise NoSpaceException(
                "No se pueden agregar estos {} items. Solo se pueden almacenar {} items mas".format(
                    cantidad, remaining_space
                )
            )
        self.stocks[nombre] = {"precio": precio, "cantidad": cantidad}
        self.total_items += cantidad

    def remueve_stock(self, nombre, cantidad):
        if cantidad <= 0:
            raise InvalidQuantityException(
                'No se puede eliminar una cantidad de {}. Debe eliminar al menos 1 item'.format(cantidad))
        if nombre not in self.stocks:
            raise ItemNotFoundException(
                'No se puede encontrar {} en nuestro stock. No se puede eliminar el stock que no existe'.format(nombre))
        if self.stocks[nombre]['cantidad'] - cantidad <= 0:
            raise InvalidQuantityException(
                'No se pueden eliminar estos {} elementos. Solo hay {} articulos en stock'.format(
                    cantidad, self.stocks[nombre]['cantidad']))
        self.stocks[nombre]['cantidad'] -= cantidad
        self.total_items -= cantidad
