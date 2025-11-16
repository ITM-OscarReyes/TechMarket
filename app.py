from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from products import load_products, get_product, create_product, update_product, delete_product
from users import verify_user, create_user, load_users, update_user, toggle_user_active

app = Flask(__name__)
app.secret_key = "supersecret"

# ------------------ AUTENTICACIÓN ------------------

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        ok, role = verify_user(request.form["username"], request.form["password"])
        if ok:
            session["user"] = request.form["username"]
            session["role"] = role
            return redirect("/products")
        return render_template("login.html", error="Credenciales inválidas")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        ok, msg = create_user(request.form["username"], request.form["password"])
        return render_template("register.html", message=msg)
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ------------------ PRODUCTOS ------------------

@app.route("/products")
def products():
    if "user" not in session:
        return redirect("/login")
    return render_template("products.html",
                           products=load_products().to_dict("records"),
                           role=session["role"])

@app.route("/products/manage")
def products_manage():
    if "user" not in session or session["role"] != "admin":
        return redirect("/products")
    return render_template("products_manage.html",
                           products=load_products().to_dict("records"),
                           role=session["role"])

@app.route("/products/new")
def product_new():
    return render_template("product_form.html", action="new", product={})

@app.route("/products/edit/<int:product_id>")
def product_edit(product_id):
    return render_template("product_form.html", action="edit", product=get_product(product_id))

# API PRODUCTOS
@app.route("/api/products", methods=["POST"])
def api_create_product():
    success, msg = create_product(request.json)
    return jsonify({"message": msg}), (201 if success else 400)

@app.route("/api/products/<int:id>", methods=["PUT"])
def api_update_product(id):
    success, msg = update_product(id, request.json)
    return jsonify({"message": msg}), (200 if success else 404)

@app.route("/api/products/<int:id>", methods=["DELETE"])
def api_delete_product(id):
    success, msg = delete_product(id)
    return jsonify({"message": msg}), (200 if success else 404)

# ------------------ ADMIN DASHBOARD ------------------

@app.route("/admin")
def admin_dashboard():
    if "user" not in session or session["role"] != "admin":
        return redirect("/products")
    return render_template("admin_dashboard.html",
                           users_count=len(load_users()),
                           products_count=len(load_products()),
                           role=session["role"])

# ------------------ USUARIOS ADMIN ------------------

@app.route("/users/manage")
def users_manage():
    if "user" not in session or session["role"] != "admin":
        return redirect("/products")
    return render_template("users_manage.html",
                           users=load_users().to_dict("records"))

@app.route("/users/new")
def user_new():
    return render_template("user_form.html", action="new", user={})

@app.route("/users/edit/<username>")
def user_edit(username):
    df = load_users()
    user = df[df["username"] == username].to_dict("records")[0]
    return render_template("user_form.html", action="edit", user=user)

# API USERS
@app.route("/api/users", methods=["POST"])
def api_create_user():
    ok, msg = create_user(request.json["username"], request.json["password"])
    return jsonify({"message": msg}), (201 if ok else 400)

@app.route("/api/users/<username>", methods=["PUT"])
def api_update_or_toggle_user(username):
    data = request.json
    if "active" in data:
        ok, msg = toggle_user_active(username, data["active"])
    else:
        ok, msg = update_user(username, data)
    return jsonify({"message": msg}), (200 if ok else 404)

# -----------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
