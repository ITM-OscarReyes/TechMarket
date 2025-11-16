# 🛒 Simulador de Tienda Online – CRUD con Python

Este proyecto es un **simulador básico de tienda online**, desarrollado como actividad académica. Incluye:  

- CRUD de productos (Crear, Leer, Actualizar, Eliminar)  
- Autenticación e inicio de sesión  
- Roles: **Administrador** y **Usuario**  
- Frontend en HTML + Bootstrap responsive  
- Backend en Python + Flask  
- Persistencia en **Excel (.xlsx)** usando pandas  
- API para operaciones de productos y usuarios  
- Validaciones tanto en frontend como en backend  
- Pruebas unitarias con **PyTest**  

---

## 📌 Funcionalidades por Rol

| Rol | Funcionalidades |
|------|----------------|
| **Administrador** | Crear, editar, eliminar y ver productos |
| **Usuario** | Ver productos solamente |
| **Ambos** | Iniciar sesión, cerrar sesión |

---

## 📁 Estructura del Proyecto

```text
TechMarket/
│
├─ app.py                   # App principal de Flask
├─ main.py                  # Lógica de usuarios y productos (CRUD)
├─ products.py              # API de productos (load/save)
├─ users.py                 # API de usuarios (load/save)
├─ requirements.txt         # Dependencias (Flask, pandas, openpyxl, pytest, werkzeug)
│
├─ data/                    # Archivos Excel (usuarios y productos)
│   ├─ products.xlsx
│   └─ users.xlsx
│
├─ templates/               # Plantillas HTML
│   ├─ admin_dashboard.html
│   ├─ layout.html
│   ├─ login.html
│   ├─ product_form.html
│   ├─ products_manage.html
│   ├─ products.html
│   ├─ register.html
│   ├─ user_form.html
│   └─ users_manage.html
│
├─ static/                  
│   ├─ main.js
│   └─ styles.css
│
└─ tests/
│   └─ products_test.py     # Pruebas unitarias CRUD de productos
│   └─ users_test.py        # Pruebas unitarias CRUD de usuarios
```

---

## 📊 Base de Datos (Excel)

- `products.xlsx` → Columnas: `id`, `name`, `description`, `price`, `quantity`  
- `users.xlsx` → Columnas: `username`, `password` (hashed), `role`, `active`  

> 💡 Cada archivo se crea automáticamente si no existe al iniciar la aplicación.

---

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el repositorio
git clone https://github.com/ITM-OscarReyes/TechMarket.git
cd TechMarket

### 2️⃣ Crear y activar entorno virtual
python -m venv venv

#### Windows
venv\Scripts\activate

#### Mac / Linux
source venv/bin/activate

### 3️⃣ Instalar dependencias
pip install -r requirements.txt

### 4️⃣ Ejecutar la aplicación
python app.py

### 5️⃣ Abrir en navegador
http://127.0.0.1:5000

---

## 🧪 Pruebas Unitarias

La carpeta `tests/` contiene pruebas para productos y usuarios, cubriendo operaciones CRUD y casos de error.

### Ejecutar todas las pruebas:
python -m pytest -v -s -W ignore::DeprecationWarning

### Explicación de los flags:
- `-v` → Muestra cada test con detalle
- `-s` → Permite ver print() en tests
- `-W ignore::DeprecationWarning` → Ignora warnings de openpyxl

---

## 🛠 Tecnologías usadas

- Python 3.x
- Flask
- Pandas + OpenPyXL (para Excel)
- HTML + Bootstrap
- PyTest (pruebas unitarias)
- Werkzeug (hash de contraseñas)
