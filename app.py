from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Product {self.name}>'


with app.app_context():
    db.create_all()


def add_sample_products():
    product1 = Product(name='Платье', quantity=15)
    product2 = Product(name='Брюки', quantity=20)
    db.session.add_all([product1, product2])
    db.session.commit()


with app.app_context():
    if Product.query.count() == 0:
        add_sample_products()


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/increase_quantity/<int:product_id>')
def increase_quantity(product_id):
    product = Product.query.filter_by(id=product_id).one_or_none()
    if product:
        product.quantity += 10
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)