from flask import url_for, flash, redirect

from functools import wraps
from flask_login import current_user


def admin_required(func):
    @wraps(func)  # Preserve metadata of the original function
    def decorated_function(*args, **kwargs):
        # Check if the user is an admin
        if current_user.role != 'admin':
            # Restrict access and redirect
            flash('Access restricted to admins only!', 'danger')
            return redirect(url_for('main_bp.index'))  # Redirect to 'index' if not admin
        return func(*args, **kwargs)  # Execute the original function if admin
    return decorated_function