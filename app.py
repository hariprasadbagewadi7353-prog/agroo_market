from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret123'

# ------------------------
# DATABASE CONFIG
# ------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# ------------------------
# MODELS
# ------------------------

class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Farmer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    price = db.Column(db.String(20))
    location = db.Column(db.String(100))
    quantity = db.Column(db.String(50))
    image = db.Column(db.String(200))

    farmer_id = db.Column(db.Integer)


    
class Scheme(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    description = db.Column(db.String(500))

    image = db.Column(db.String(200))
    video = db.Column(db.String(200))






class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(100))

    product_name = db.Column(db.String(100))

    address = db.Column(db.String(300))

    status = db.Column(
        db.String(50),
        default="Order Placed"
    )
     
# ------------------------
# HOME
# ------------------------

@app.route('/')
def home():

    return render_template("index.html")







# ------------------------
# ADD SCHEME
# ------------------------

@app.route('/add_scheme', methods=['GET', 'POST'])
def add_scheme():

    # admin only
    if 'admin' not in session:
        return redirect('/login_admin')

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')

        # IMAGE
        image_file = request.files.get('image')
        image_name = ""

        if image_file and image_file.filename != "":

            image_name = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                image_name
            )

            image_file.save(image_path)

        # VIDEO
        video_file = request.files.get('video')
        video_name = ""

        if video_file and video_file.filename != "":

            video_name = secure_filename(video_file.filename)

            video_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                video_name
            )

            video_file.save(video_path)

        # SAVE SCHEME
        new_scheme = Scheme(
            title=title,
            description=description,
            image=image_name,
            video=video_name
        )

        db.session.add(new_scheme)
        db.session.commit()

        flash("Scheme Added Successfully ✅")

        return redirect('/show_schemes')

    return render_template("add_scheme.html")








# ------------------------
# ADMIN LOGIN
# ------------------------

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():

    if 'admin' in session:
        return redirect('/admin_dashboard')

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:

            session['admin'] = admin.username
            session.modified = True

            flash("Admin Login Successful ✅")

            return redirect('/admin_dashboard')

        else:

            flash("Invalid Admin Login ❌")

    return render_template("login_admin.html")


# ------------------------
# FARMER LOGIN
# ------------------------

@app.route('/login_farmer', methods=['GET', 'POST'])
def login_farmer():

    if 'farmer' in session:
        return redirect('/farmer_dashboard')

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        farmer = Farmer.query.filter_by(
            username=username,
            password=password
        ).first()

        if farmer:

            session['farmer'] = farmer.username
            session['farmer_id'] = farmer.id

            session.modified = True

            flash("Farmer Login Successful ✅")

            return redirect('/farmer_dashboard')

        else:

            flash("Invalid Farmer Login ❌")

    return render_template("login_farmer.html")


# ------------------------
# CUSTOMER LOGIN
# ------------------------

@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        customer = Customer.query.filter_by(
            username=username,
            password=password
        ).first()

        if customer:

            session['customer'] = customer.username
            session['customer_id'] = customer.id

            flash("Customer Login Successful ✅")

            return redirect('/show_products')

        else:

            flash("Invalid Customer Login ❌")

    return render_template("login_customer.html")


# ------------------------
# REGISTER FARMER
# ------------------------

@app.route('/register_farmer', methods=['GET', 'POST'])
def register_farmer():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        farmer = Farmer(
            username=username,
            password=password
        )

        db.session.add(farmer)
        db.session.commit()

        flash("Farmer Registered Successfully ✅")

        return redirect('/login_farmer')

    return render_template("register_farmer.html")


# ------------------------
# REGISTER CUSTOMER
# ------------------------

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        customer = Customer(
            username=username,
            password=password
        )

        db.session.add(customer)
        db.session.commit()

        flash("Customer Registered Successfully ✅")

        return redirect('/login_customer')

    return render_template("register_customer.html")


# ------------------------
# DASHBOARDS
# ------------------------

@app.route('/admin_dashboard')
def admin_dashboard():

    if session.get('admin') is None:
        return redirect('/login_admin')

    return render_template("admin_dashboard.html")


@app.route('/farmer_dashboard')
def farmer_dashboard():

    if session.get('farmer') is None:
        return redirect('/login_farmer')

    return render_template("farmer_dashboard.html")


# ------------------------
# ADD PRODUCT
# ------------------------

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    if 'farmer' not in session:
        return redirect('/login_farmer')

    if request.method == 'POST':

        name = request.form.get('name')
        price = request.form.get('price')
        location = request.form.get('location')
        quantity = request.form.get('quantity')

        image_file = request.files.get('image')

        image_name = None

        if image_file and image_file.filename != "":

            image_name = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                image_name
            )

            image_file.save(image_path)

        product = Product(
            name=name,
            price=price,
            location=location,
            quantity=quantity,
            image=image_name,
            farmer_id=session.get('farmer_id')
        )

        db.session.add(product)
        db.session.commit()

        flash("Product Added Successfully ✅")

        return redirect(url_for('show_products'))

    return render_template("products.html")


# ------------------------
# SHOW PRODUCTS
# ------------------------

@app.route('/show_products')
def show_products():

    products = Product.query.all()

    return render_template(
        "show_product.html",
        products=products
    )


# ------------------------
# DELETE PRODUCT
# ------------------------

@app.route('/delete_product/<int:id>')
def delete_product(id):

    if 'farmer' not in session:

        flash("Access Denied ❌")

        return redirect(url_for('show_products'))

    product = Product.query.get_or_404(id)

    if product.farmer_id != session.get('farmer_id'):

        flash("You can delete only your products ❌")

        return redirect(url_for('show_products'))

    if product.image:

        image_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            product.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()

    flash("Product Deleted Successfully 🗑️")

    return redirect(url_for('show_products'))


# ------------------------
# ADD SCHEME
# -----------@app.route('/add_scheme', methods=['GET', 'POST'])
def add_scheme():

    if 'admin' not in session:
        return redirect('/login_admin')

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')

        # IMAGE
        image_file = request.files.get('image')
        image_name = ""

        if image_file and image_file.filename != "":
            image_name = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                image_name
            )

            image_file.save(image_path)

        # VIDEO
        video_file = request.files.get('video')
        video_name = ""

        if video_file and video_file.filename != "":
            video_name = secure_filename(video_file.filename)

            video_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                video_name
            )

            video_file.save(video_path)

        new_scheme = Scheme(
            title=title,
            description=description,
            image=image_name,
            video=video_name
        )

        db.session.add(new_scheme)
        db.session.commit()

        flash("Scheme Added Successfully ✅")

        return redirect('/show_schemes')

    return render_template("add_scheme.html")
# ------------------------
# SHOW SCHEMES
# ------------------------

@app.route('/show_schemes')
def show_schemes():

    schemes = Scheme.query.all()

    return render_template(
        "show_schemes.html",
        schemes=schemes
    )


# ========================
# CART SYSTEM
# ========================

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):

    if 'customer' not in session:
        return redirect('/login_customer')

    cart = session.get('cart', [])

    if id not in cart:
        cart.append(id)

    session['cart'] = cart

    flash("Added To Cart 🛒")

    return redirect(url_for('show_products'))


@app.route('/cart')
def cart():

    if 'customer' not in session:
        return redirect('/login_customer')

    ids = session.get('cart', [])

    products = []

    if ids:

        products = Product.query.filter(
            Product.id.in_(ids)
        ).all()

    return render_template(
        "cart.html",
        products=products
    )


@app.route('/remove/<int:id>')
def remove(id):

    cart = session.get('cart', [])

    if id in cart:
        cart.remove(id)

    session['cart'] = cart

    flash("Product Removed ❌")

    return redirect(url_for('cart'))


# ========================
# BUY SYSTEM
# ========================

@app.route('/buy/<int:id>')
def buy(id):

    if 'customer' not in session:
        return redirect('/login_customer')

    product = Product.query.get_or_404(id)

    return render_template(
        "checkout.html",
        products=[product]
    )


@app.route('/checkout')
def checkout():

    if 'customer' not in session:
        return redirect('/login_customer')

    ids = session.get('cart', [])

    products = []

    if ids:

        products = Product.query.filter(
            Product.id.in_(ids)
        ).all()

    return render_template(
        "checkout.html",
        products=products
    )


# ------------------------
# PLACE ORDER
# ------------------------
@app.route('/place_order', methods=['POST'])
def place_order():

    ids = session.get('cart', [])

    products = Product.query.filter(
        Product.id.in_(ids)
    ).all()

    for p in products:

        order = Order(

            customer_name=session.get('customer'),

            product_name=p.name,

            address="Customer Address",

            status="Order Placed"
        )

        db.session.add(order)

    db.session.commit()

    session.pop('cart', None)

    flash("Order Placed Successfully ✅")

    return redirect('/my_orders')


@app.route('/my_orders')
def my_orders():

    if 'customer' not in session:
        return redirect('/login_customer')

    orders = Order.query.filter_by(
        customer_name=session.get('customer')
    ).all()

    return render_template(
        "my_orders.html",
        orders=orders
    )



@app.route('/update_status/<int:id>/<status>')
def update_status(id, status):

    if 'admin' not in session:
        return redirect('/login_admin')

    order = Order.query.get_or_404(id)

    order.status = status

    db.session.commit()

    return redirect('/manage_orders')





@app.route('/manage_orders')
def manage_orders():

    if 'admin' not in session:
        return redirect('/login_admin')

    orders = Order.query.all()

    return render_template(
        "manage_orders.html",
        orders=orders
    )
# ------------------------
# LOGOUT
# ------------------------

@app.route('/logout')
def logout():

    session.clear()

    flash("Logged Out Successfully 👋")

    return redirect('/')


# ------------------------
# RUN
# ------------------------

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        # default admin
        if not Admin.query.filter_by(username='admin').first():

            admin = Admin(
                username='admin',
                password='admin123'
            )

            db.session.add(admin)
            db.session.commit()

            print("Default Admin Created")

    app.run(debug=True)