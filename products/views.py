from flask import Blueprint, render_template, request, redirect, url_for, flash
from extentions import db
from .models import Product

product_bp = Blueprint('product_bp', __name__, url_prefix='/product', template_folder='templates')

# Product list + Create new product (via modal form submission on this page)
@product_bp.route('/', methods=['GET', 'POST'])
def product_list():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            description=request.form.get('description', ''),
            price=float(request.form['price']),
            image_url=request.form.get('image_url', ''),
            quantity=int(request.form.get('quantity', 0))
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product_bp.product_list'))

    products = Product.query.all()
    return render_template('products.html', products=products)


# Edit product (regular separate route)
@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form.get('description', '')
        product.price = float(request.form['price'])
        product.image_url = request.form.get('image_url', '')
        product.quantity = int(request.form.get('quantity', 0))
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_bp.product_list'))

    return render_template('products_edit.html', product=product)


# Delete product (regular separate route)
@product_bp.route('/delete/<int:product_id>', methods=['GET', 'POST'])
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted.', 'info')
        return redirect(url_for('product_bp.product_list'))

    return render_template('products_delete.html', product=product)
