import pandas as pd
import os

FILE_PATH = "data/products.xlsx"

def load_products():
    folder = os.path.dirname(FILE_PATH)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["id","name","description","price","quantity"])
        df.to_excel(FILE_PATH, index=False)
        return df

    return pd.read_excel(FILE_PATH)

def save_products(df):
    df.to_excel(FILE_PATH, index=False)

def get_product(product_id):
    df = load_products()
    item = df[df["id"] == product_id]
    return item.iloc[0].to_dict() if not item.empty else None

def create_product(data):
    df = load_products()
    if data["id"] in df["id"].values:
        return False, "ID ya existe"

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    save_products(df)
    return True, "Producto creado correctamente"

def update_product(product_id, data):
    df = load_products()

    if product_id not in df["id"].values:
        return False, "Producto no encontrado"

    index = df[df["id"] == product_id].index[0]

    df.at[index, "name"] = data.get("name")
    df.at[index, "description"] = data.get("description")
    df.at[index, "price"] = data.get("price")
    df.at[index, "quantity"] = data.get("quantity")

    save_products(df)
    return True, "Producto actualizado correctamente"


def delete_product(product_id):
    df = load_products()
    if product_id not in df["id"].values:
        return False, "Producto no existe"

    df = df[df["id"] != product_id]
    save_products(df)
    return True, "Producto eliminado correctamente"
