import os
import sqlite3
from flask import Flask, render_template, g, redirect, url_for
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'market.db'),
))


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')


@app.route('/')
def catalog():
    db = get_db()
    cur = db.execute('select * from products order by id desc')
    products = cur.fetchall()
    cur = db.execute('select count(id) as count from products')
    count = cur.fetchone()
    return render_template('catalog.html', products=products, count=count)


@app.route('/product/<int:product_id>')
def product_page(product_id):
    db = get_db()
    cur = db.execute('select * from products where id = ? order by id desc', [product_id])
    product = cur.fetchone()
    return render_template('product_page.html', product=product)


@app.route('/add-products')
def add_products():
    db = get_db()
    db.execute('insert into products (title, price, image1, description) values (?, ?, ?, ?)',
               ['Xiaomi Redmi 4X 32GB', 9500, 'images/3.jpeg',
                'смартфон, Android 6.0; поддержка двух SIM-карт; экран 5", разрешение 1280x720; камера 13 МП, автофокус; память 32 Гб, слот для карты памяти; 3G, 4G LTE, LTE-A, Wi-Fi, Bluetooth, GPS, ГЛОНАСС; объем оперативной памяти 3 Гб; аккумулятор 4100 мА⋅ч; вес 150 г, ШxВxТ 69.96x139.24x8.65 мм'])
    db.commit()
    db.execute('insert into products (title, price, image1, description) values (?, ?, ?, ?)',
               ['Apple iPhone 8 64GB', 56990, 'images/4.jpeg',
                'смартфон, iOS 11; экран 4.7", разрешение 1334x750; камера 12 МП, автофокус, F/1.8; память 64 Гб, без слота для карт памяти; 3G, 4G LTE, LTE-A, Wi-Fi, Bluetooth, NFC, GPS, ГЛОНАСС; вес 148 г, ШxВxТ 67.30x138.40x7.30 мм'])
    db.commit()
    return redirect(url_for('catalog'))