from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(user_id=current_user.id, text=note)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for("views.home"))
    return render_template("index.html", user=current_user, notes=notes)

@views.route("/delete-note/<id>", methods=["GET", "POST"])
@login_required
def delete_note(id):
    note = Note.query.get(int(id))
    if note:
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for("views.home"))
    