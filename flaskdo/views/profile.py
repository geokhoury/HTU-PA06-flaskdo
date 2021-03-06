import sqlite3
from flask import Blueprint, render_template, request, redirect, session, url_for
from ..models.user import User
from ..db import get_db

# define our blueprint
bp = Blueprint('profile', __name__)


@bp.route('/profile')
def view_profile():
    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        user = db.execute(
            "SELECT * FROM User WHERE id=?;", (session['uid'],)).fetchone()

        # if the user was found
        if user:
            # redirect to index
            return render_template('profile/profile.html', user=user)
        # if the user was not found
        else:
            # render the login page with an error message
            return redirect("/404")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/edit/profile', methods=['GET', 'POST'])
def edit_profile():
    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        user = db.execute(
            "SELECT * FROM User WHERE id=?;", (session['uid'],)).fetchone()

        # if the user was found
        if user:
            if request.method == 'GET':
                # redirect to index
                return render_template('profile/edit-profile.html', user=user)
            else:
                email = request.form['email']
                first_name = request.form['first-name']
                last_name = request.form['last-name']
                birthdate = request.form['birthdate']
                avatarURL = request.form['avatarURL']
                address = request.form['address']

                db.execute(
                    "UPDATE User SET email=?, first_name=?, last_name=?, birthdate=?, avatarURL=?, address=? WHERE id=?;", (email, first_name, last_name, birthdate, avatarURL, address, session['uid'],)).fetchone()

                db.commit()
                return redirect(url_for('profile.view_profile'))
        # if the user was not found
        else:
            # render the login page with an error message
            return redirect("/404")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")


@bp.route('/delete/profile')
def delete_profile():

    # get db connection
    db = get_db()

    # fetch user
    try:
        # execute the SQL query
        db.execute("DELETE FROM User WHERE id=?;", (session['uid'],))
        db.commit()

        return redirect(url_for("login.logout"))

    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        return redirect("/404")
