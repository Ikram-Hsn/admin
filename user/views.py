from flask import Blueprint, render_template, request, redirect, url_for, abort
from extentions import db
from user.models import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/user', template_folder='templates')

@user_bp.route('/')
def user_list():
    users = User.query.all()
    return render_template('users.html', users=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        user_status = "user_status" in request.form
        new_user = User(
            username=request.form['username'],
            full_name=request.form['full_name'],
            email=request.form['email'],
            user_type=request.form['user_type'],
            is_active=user_status
        )
        new_user.save()
        return redirect(url_for('user_bp.user_list'))
    return render_template('users_add.html')

@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.full_name = request.form['full_name']
        user.email = request.form['email']
        user.user_type = request.form['user_type']
        user.is_active = 'user_status' in request.form
        user.update()
        return redirect(url_for('user_bp.user_list'))

    return render_template('users_edit.html', user=user)

@user_bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.delete()
        return redirect(url_for('user_bp.user_list'))
    return render_template('users_delete.html', user=user)
