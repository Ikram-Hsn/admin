from flask import Blueprint, render_template, request, redirect, url_for, flash
from extentions import db
from customer.models import Customer

customer_bp = Blueprint('customer_bp', __name__, url_prefix='/customer', template_folder='templates')

@customer_bp.route('/')
def customer_list():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@customer_bp.route('/add', methods=['GET', 'POST'])
def customer_add():
    if request.method == 'POST':
        is_active = "is_active" in request.form
        new_customer = Customer(
            username=request.form['username'],
            full_name=request.form['full_name'],
            email=request.form['email'],
            user_type=request.form['user_type'],
            is_active=is_active
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully.', 'success')
        return redirect(url_for('customer_bp.customer_list'))
    return render_template('customers_add.html')

@customer_bp.route('/edit/<int:customer_id>', methods=['GET', 'POST'])
def customer_edit(customer_id):
    data = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        data.username = request.form['username']
        data.full_name = request.form['full_name']
        data.email = request.form['email']
        data.user_type = request.form['user_type']
        data.is_active = 'is_active' in request.form

        db.session.commit()
        flash('Customer updated successfully.', 'success')
        return redirect(url_for('customer_bp.customer_list'))
    return render_template('customers_edit.html', customer=data)



@customer_bp.route('/delete/<int:customer_id>', methods=['GET', 'POST'])
def customer_delete(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        db.session.delete(customer)  # use db.session.delete
        db.session.commit()
        flash('Customer deleted successfully.', 'success')
        return redirect(url_for('customer_bp.customer_list'))
    return render_template('customers_delete.html', customer=customer)
