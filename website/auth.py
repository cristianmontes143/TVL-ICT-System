from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from . import supabase
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        try:
            # Attempt to sign in with email and password
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            print(response)

            # Check for errors in the response
            if response.error:
                flash(f"Error: {response.error.message}", 'error')
            else:
                session['user'] = response.data['user']
                return redirect(url_for('views.home'))
        
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')

    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password1')  # assuming password1 is the password field
        

        # Validate email format
        if not is_valid_email(email):
            flash("Invalid email address format.", 'error')
            return render_template("sign_up.html")

        # Attempt to sign up the user
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})

            if response.error:
                flash(response.error.message, 'error')
            else:
                user = response.data['user']
                supabase.table('users').insert({"id": user['id'], "email": email, "first_name": first_name}).execute()
                session['user'] = user
                return redirect(url_for('views.home'))
        except Exception as e:
            flash(f"An error occurred: {e}", 'error')

    return render_template("sign_up.html")
