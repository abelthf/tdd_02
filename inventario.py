class Inventario:
    def __init__(self, limite=100):
        self.limite = limite
        self.total_items = 0
        self.stocks = {}

    def add_nuevo_stock(self, nombre, precio, cantidad):
        self.stocks[nombre] = {
                'precio': precio,
                'cantidad': cantidad
                }
        self.total_items += cantidad

