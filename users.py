import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash

FILE_PATH = "data/users.xlsx"

def load_users():
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=["username","password","role","active"])
        df.to_excel(FILE_PATH, index=False)

    df = pd.read_excel(FILE_PATH)

    if "active" not in df.columns:
        df["active"] = 1
        save_users(df)

    df['username'] = df['username'].astype(str)
    df['role'] = df['role'].astype(str)
    df['active'] = df['active'].astype(int)
    df['password'] = df['password'].astype(str)

    return df

def save_users(df):
    df.to_excel(FILE_PATH, index=False)

def create_user(username, password):
    df = load_users()
    if username in df["username"].values:
        return False, "El usuario ya existe"

    hashed_pw = generate_password_hash(password)
    new_user = {
        "username": username,
        "password": hashed_pw,
        "role": "user",
        "active": 1
    }

    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    save_users(df)
    return True, "Usuario creado correctamente"

def verify_user(username, password):
    df = load_users()

    if username not in df["username"].values:
        return False, None

    row = df[df["username"] == username].iloc[0]

    if row["active"] == 0:
        return False, None

    if check_password_hash(row["password"], password):
        return True, row["role"]
    else:
        return False, None

def update_user(username, data):
    df = load_users()

    if username not in df["username"].values:
        return False, "Usuario no encontrado"

    if "role" in data:
        df.loc[df["username"] == username, "role"] = data["role"]
    if "active" in data:
        df.loc[df["username"] == username, "active"] = data["active"]

    save_users(df)
    return True, "Usuario actualizado"

def toggle_user_active(username, estado: int) -> tuple[bool, str]:
    df = load_users()
    if username not in df["username"].values:
        return False, "Usuario no encontrado"

    df.loc[df["username"] == username, "active"] = estado
    save_users(df)
    return True, "Usuario actualizado"
