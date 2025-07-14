from forms import LoginForm, RegistrationForm, ProductForm
from ext import app, db
from models import Product, User
import os
from flask import render_template, redirect, flash, abort, url_for, session
from flask_login import login_user, logout_user, login_required, current_user

def get_cart_items():
    return session.get('cart', [])


profiles = []

products = []
products1 = []


@app.route("/")
def home():
    role = "user"
    cart_items = len(get_cart_items())
    products_db = Product.query.all()

    return render_template(
        "var3.html",
        productebi=products_db,
        productebia=products1,
        role=role,
        cart_items=cart_items,
        products=products_db)


@app.route("/cart")
def cart():
    cart_product_ids = get_cart_items()
    length = len(cart_product_ids)

    if cart_product_ids:
        products = Product.query.filter(Product.id.in_(cart_product_ids)).all()
    else:
        products = []

    total_price = sum(product.price for product in products)

    return render_template('cart.html', products=products, cart_items=length, total_price=total_price)


@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
def add_to_cart(item_id):
    cart = session.get('cart', [])
    if item_id not in cart:
        cart.append(item_id)
    session['cart'] = cart
    return redirect("/cart")


@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    if item_id in cart:
        cart.remove(item_id)
        session['cart'] = cart
    return redirect("/cart")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("მომხმარებელი უკვე არსებობს!", "danger")
            return render_template("register.html", form=form)

        role = "Admin" if form.username.data.lower() == "admin" else "Guest"

        new_user = User(
            username=form.username.data,
            password=form.password.data,
            gender=form.gender.data,
            birthday=form.birthday.data.strftime('%Y-%m-%d'),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash("რეგისტრაცია წარმატებით შესრულდა!", "success")
        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    if current_user.role != "Admin":
        abort(403)

    form = ProductForm()

    if form.validate_on_submit():
        image = form.img.data
        filename = image.filename
        upload_folder = os.path.join(app.root_path, "static", "images")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        path = os.path.join(upload_folder, filename)
        image.save(path)

        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            img=filename
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('view_product', product_id=new_product.id))

    return render_template("create_product.html", form=form)

@app.route("/delete_product/<int:product1_id>")
@login_required
def delete_product(product1_id):
    if current_user.role != "Admin":
        abort(403)
    product = Product.query.get(product1_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect("/")


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "Admin":
        abort(403)
    product = Product.query.get(product_id)
    if not product:
        return "Product not found", 404

    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

       if form.img.data and hasattr(form.img.data, 'filename'):
            image = form.img.data
            filename = image.filename
            upload_folder = os.path.join(app.root_path, "static", "images")

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            path = os.path.join(upload_folder, filename)
            image.save(path)
            product.img = filename

        db.session.commit()
        return redirect("/")

    return render_template("create_product.html", form=form)

@app.route("/branches")
def branches():
    return render_template("branches.html")


@app.route("/deliver")
def deliver():
    return render_template("deliver.html")


@app.route("/buy")
def buy():
    session['cart'] = []
    return render_template("buy.html")


@app.route('/products/<int:product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('view_product.html', product=product)

