from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from . import supabase
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = session['user']
    
    # Ensure 'notes' key exists
    notes_response = supabase.table('notes').select('*').eq('user_id', user['id']).execute()
    notes = notes_response.data if notes_response else []

    return render_template("home.html", user=user, notes=notes)

@views.route('/add-note', methods=['POST'])
def add_note():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    note = request.form.get('note')
    user_id = session['user']['id']

    supabase.table('notes').insert({"data": note, "user_id": user_id}).execute()
    flash('Note added!', 'success')
    return redirect(url_for('views.home'))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 403

    note_id = request.json.get('noteId')
    supabase.table('notes').delete().eq('id', note_id).execute()
    return jsonify({"success": True})
