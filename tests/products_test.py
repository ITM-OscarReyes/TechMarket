import pytest
from products import create_product, get_product, update_product, delete_product

@pytest.fixture(autouse=True)
def usar_tmp_path(tmp_path, monkeypatch):
    test_file = tmp_path / "products.xlsx"
    monkeypatch.setattr("products.FILE_PATH", str(test_file))

def test_agregar_producto():
    ok, msg = create_product({"id": 1, "name":"P1","description":"x","price":10,"quantity":5})
    resultado = f"Agregado: 1 -> P1" if ok else f"Error: {msg}"
    assert resultado == "Agregado: 1 -> P1"
    prod = get_product(1)
    assert prod["name"] == "P1"

def test_agregar_producto_duplicado():
    create_product({"id": 2, "name":"P2","description":"y","price":20,"quantity":1})
    ok, msg = create_product({"id": 2, "name":"P2","description":"y","price":20,"quantity":1})
    resultado = f"Agregado: 2 -> P2" if ok else f"Error: {msg}"
    assert resultado == "Error: ID ya existe"

def test_consultar_producto_existente():
    create_product({"id":3,"name":"P3","description":"z","price":15,"quantity":2})
    prod = get_product(3)
    resultado = f"Consultado: 3 -> {prod['name']}" if prod else "Clave no encontrada"
    assert resultado == "Consultado: 3 -> P3"

def test_consultar_producto_no_existente():
    prod = get_product(999)
    resultado = f"Consultado: 999 -> {prod['name']}" if prod else "Clave no encontrada"
    assert resultado == "Clave no encontrada"

def test_modificar_producto_existente():
    create_product({"id":4,"name":"P4","description":"d","price":5,"quantity":1})
    ok, msg = update_product(4, {"name":"P4X","price":50,"description":"d","quantity":1})
    resultado = f"Modificado: 4 -> P4X" if ok else "Clave no encontrada"
    assert resultado == "Modificado: 4 -> P4X"
    prod = get_product(4)
    assert prod["name"] == "P4X"
    assert prod["price"] == 50

def test_modificar_producto_no_existente():
    ok, msg = update_product(999, {"name":"X"})
    resultado = f"Modificado: 999 -> X" if ok else "Clave no encontrada"
    assert resultado == "Clave no encontrada"

def test_eliminar_producto_existente():
    create_product({"id":5,"name":"P5","description":"q","price":8,"quantity":2})
    ok, msg = delete_product(5)
    resultado = f"Eliminado: 5" if ok else "Clave no encontrada"
    assert resultado == "Eliminado: 5"
    assert get_product(5) is None

def test_eliminar_producto_no_existente():
    ok, msg = delete_product(999)
    resultado = f"Eliminado: 999" if ok else "Clave no encontrada"
    assert resultado == "Clave no encontrada"