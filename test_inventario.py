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
    inventario.remueve_stock('patanlones adidas', 1)
    assert inventario.total_items == 12
