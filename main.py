import os
import pandas as pd
from typing import Dict, Any, List

# Carpetas de datos (productos y usuarios)
DATA_DIR = "data"
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.xlsx")
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")

PRODUCT_COLUMNS = ["id", "nombre", "descripcion", "precio", "cantidad"]
USER_COLUMNS = ["username", "password", "role", "active"]

# Permitir cambiar la carpeta para tests
def set_data_dir(path: str):
    global DATA_DIR, PRODUCTS_FILE, USERS_FILE
    DATA_DIR = path
    PRODUCTS_FILE = os.path.join(DATA_DIR, "products.xlsx")
    USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")

# -------------------
# Usuarios
# -------------------
def ensure_users_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=USER_COLUMNS)
        df.to_excel(USERS_FILE, index=False)

def cargar_usuarios() -> pd.DataFrame:
    ensure_users_file()
    return pd.read_excel(USERS_FILE)

def guardar_usuarios(df: pd.DataFrame) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(USERS_FILE, index=False)

def create_user(username, password, role="user") -> tuple[bool, str]:
    df = cargar_usuarios()
    if username in df["username"].values:
        return False, "El usuario ya existe"
    df = pd.concat([df, pd.DataFrame([{
        "username": username,
        "password": password,
        "role": role,
        "active": 1
    }])], ignore_index=True)
    guardar_usuarios(df)
    return True, "Usuario creado correctamente"

def verify_user(username, password) -> tuple[bool, str]:
    df = cargar_usuarios()
    sel = df[(df["username"] == username) & (df["password"] == password) & (df["active"] == 1)]
    if sel.empty:
        return False, ""
    return True, sel.iloc[0]["role"]

def update_user(username, nuevos_datos: Dict[str, Any]) -> tuple[bool, str]:
    df = cargar_usuarios()
    if username not in df["username"].values:
        return False, "Usuario no encontrado"
    for k, v in nuevos_datos.items():
        if k in USER_COLUMNS and k != "username":
            df.loc[df["username"] == username, k] = v
    guardar_usuarios(df)
    return True, "Usuario actualizado"

def toggle_user_active(username, estado: int) -> tuple[bool, str]:
    df = cargar_usuarios()
    if username not in df["username"].values:
        return False, "Usuario no encontrado"
    df.loc[df["username"] == username, "active"] = estado
    guardar_usuarios(df)
    return True, "Usuario actualizado"

# -------------------
# Productos
# -------------------
def ensure_products_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PRODUCTS_FILE):
        df = pd.DataFrame(columns=PRODUCT_COLUMNS)
        df.to_excel(PRODUCTS_FILE, index=False)

def cargar_productos() -> pd.DataFrame:
    ensure_products_file()
    return pd.read_excel(PRODUCTS_FILE)

def guardar_productos(df: pd.DataFrame) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(PRODUCTS_FILE, index=False)

def listar_todos_productos() -> List[Dict[str, Any]]:
    return cargar_productos().to_dict(orient="records")

def obtener_producto_por_id(prod_id) -> Dict[str, Any] | None:
    df = cargar_productos()
    sel = df[df["id"] == prod_id]
    return sel.iloc[0].to_dict() if not sel.empty else None

def agregar_producto(producto: Dict[str, Any]) -> str:
    df = cargar_productos()
    if producto["id"] in df["id"].values:
        return "Error: ID ya existe"
    row = {
        "id": producto["id"],
        "nombre": producto.get("nombre", ""),
        "descripcion": producto.get("descripcion", ""),
        "precio": float(producto.get("precio", 0)),
        "cantidad": int(producto.get("cantidad", 0)),
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    guardar_productos(df)
    return "Producto agregado"

def modificar_producto(prod_id, nuevos_datos: Dict[str, Any]) -> str:
    df = cargar_productos()
    if prod_id not in df["id"].values:
        return "Producto no encontrado"
    for k, v in nuevos_datos.items():
        if k in PRODUCT_COLUMNS and k != "id":
            df.loc[df["id"] == prod_id, k] = v
    guardar_productos(df)
    return "Producto actualizado"

def eliminar_producto(prod_id) -> str:
    df = cargar_productos()
    if prod_id not in df["id"].values:
        return "Producto no encontrado"
    df = df[df["id"] != prod_id]
    guardar_productos(df)
    return "Producto eliminado"