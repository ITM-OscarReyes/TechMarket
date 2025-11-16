import pytest
from users import create_user, verify_user, update_user, toggle_user_active, load_users

@pytest.fixture(autouse=True)
def usar_tmp_path(tmp_path, monkeypatch):
    test_file = tmp_path / "users.xlsx"
    monkeypatch.setattr("users.FILE_PATH", str(test_file))

def test_create_user_success():
    ok, msg = create_user("juan", "clave123")
    resultado = f"Agregado: juan" if ok else f"Error: {msg}"
    assert resultado == "Agregado: juan"

    ok2, role = verify_user("juan", "clave123")
    resultado2 = f"Verificado: juan -> {role}" if ok2 else "Clave no encontrada"
    assert resultado2 == "Verificado: juan -> user"

def test_create_user_duplicate():
    create_user("ana", "pass")
    ok, msg = create_user("ana", "otra")
    resultado = f"Agregado: ana" if ok else f"Error: {msg}"
    assert resultado == "Error: El usuario ya existe"

def test_update_user_success():
    create_user("maria","1234")
    ok, msg = update_user("maria", {"role":"admin","active":1})
    resultado = f"Modificado: maria -> admin" if ok else "Clave no encontrada"
    assert resultado == "Modificado: maria -> admin"

    df = load_users()
    user = df[df["username"]=="maria"].iloc[0]
    assert user["role"]=="admin"

def test_update_user_not_found():
    ok, msg = update_user("ghost", {"role":"user"})
    resultado = f"Modificado: ghost -> user" if ok else "Clave no encontrada"
    assert resultado == "Clave no encontrada"

def test_toggle_user_active():
    create_user("luis","pass")

    ok, msg = toggle_user_active("luis",0)
    resultado = f"Modificado: luis -> inactivo" if ok else "Clave no encontrada"
    assert resultado == "Modificado: luis -> inactivo"
    ok_auth, _ = verify_user("luis","pass")
    resultado_auth = "Usuario activo" if ok_auth else "Usuario inactivo"
    assert resultado_auth == "Usuario inactivo"

    ok2, msg2 = toggle_user_active("luis",1)
    resultado2 = f"Modificado: luis -> activo" if ok2 else "Clave no encontrada"
    assert resultado2 == "Modificado: luis -> activo"
    ok_auth2,_ = verify_user("luis","pass")
    resultado_auth2 = "Usuario activo" if ok_auth2 else "Usuario inactivo"
    assert resultado_auth2 == "Usuario activo"

def test_toggle_user_not_found():
    ok, msg = toggle_user_active("nadie",0)
    resultado = f"Modificado: nadie -> inactivo" if ok else "Clave no encontrada"
    assert resultado == "Clave no encontrada"
