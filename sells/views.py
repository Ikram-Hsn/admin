from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from customer.models import Customer
from extentions import db
from .models import Sell
from products.models import Product

sell_bp = Blueprint('sell_bp', __name__, url_prefix='/sell', template_folder='templates')

@sell_bp.route('/')
def sell_list():
    sells = Sell.query.all()
    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('sells.html', sells=sells, customer=customers, products=products)

@sell_bp.route('/add', methods=['GET', 'POST'])
def sell_add():
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        product_id = int(request.form['product_id'])
        description = request.form['description']
        quantity = int(request.form['quantity'])
        total_price = float(request.form['total_price'])

        new_sell = Sell(
            customer_id=customer_id,
            product_id=product_id,
            description=description,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(new_sell)
        db.session.commit()
        flash('Sell added successfully!', 'success')
        return redirect(url_for('sell_bp.sell_list'))

    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('sells_add.html', customers=customers, products=products)


# ...  edit sells...
@sell_bp.route('/edit/<int:sell_id>', methods=['GET', 'POST'])
def sell_edit(sell_id):
    sell = Sell.query.get_or_404(sell_id)
    customers = Customer.query.all()
    products = Product.query.all()

    if request.method == 'POST':
        sell.customer_id = int(request.form['customer_id'])
        sell.product_id = int(request.form['product_id'])
        sell.description = request.form['description']
        sell.quantity = int(request.form['quantity'])
        sell.total_price = float(request.form['total_price'])

        db.session.commit()
        flash('Sell updated successfully!', 'success')
        return redirect(url_for('sell_bp.sell_list'))

    return render_template('sells_edit.html', sell=sell, customers=customers, products=products)


@sell_bp.route('/delete/<int:sell_id>', methods=['GET', 'POST'])
def delete_sell(sell_id):
    sell = Sell.query.get_or_404(sell_id)

    if request.method == 'POST':
        try:
            db.session.delete(sell)
            db.session.commit()
            flash('Sell deleted successfully!', 'success')
            return redirect(url_for('sell_bp.sell_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting sell: {e}', 'danger')
            return redirect(url_for('sell_bp.sell_list'))

    # GET request: show confirmation form with sell info
    return render_template('sells._delete.html', sell=sell)

