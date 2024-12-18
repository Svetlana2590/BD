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


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)