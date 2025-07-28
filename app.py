from flask import Flask, render_template
from extentions import db
from user.views import user_bp
from customer.views import customer_bp
from products.views import product_bp
from sells.views import sell_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-very-secret-key-here'  # Use a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@127.0.0.1/third_databased'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(product_bp)
app.register_blueprint(sell_bp)


@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables from your models
    app.run(debug=True, port=5001)
