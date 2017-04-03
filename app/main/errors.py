from flask import render_template, redirect, url_for
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(401)
def unauthorized(e):
    return redirect(url_for('auth.login'))

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
