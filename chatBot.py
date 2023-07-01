from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'notes.db'

# Helper function to establish database connection
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# API endpoint to create a new note
@app.route('/notes', methods=['POST'])
def create_note():
    content = request.json.get('content')

    if not content:
        return jsonify({'error': 'Note content is required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    note_id = cursor.lastrowid
    db.commit()
    db.close()

    return jsonify({'id': note_id, 'content': content}), 201

# API endpoint to retrieve all notes
@app.route('/notes', methods=['GET'])
def get_all_notes():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    db.close()

    results = []
    for note in notes:
        results.append({'id': note['id'], 'content': note['content']})

    return jsonify(results), 200

# API endpoint to retrieve a specific note
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note_by_id(note_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = cursor.fetchone()
    db.close()

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({'id': note['id'], 'content': note['content']}), 200

# API endpoint to update a specific note
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note_by_id(note_id):
    content = request.json.get('content')

    if not content:
        return jsonify({'error': 'Note content is required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE notes SET content = ? WHERE id = ?', (content, note_id))
    db.commit()
    db.close()

    return jsonify({'message': 'Note updated successfully'}), 200

# API endpoint to delete a specific note
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note_by_id(note_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    db.commit()
    db.close()

    return jsonify({'message': 'Note deleted successfully'}), 200

if __name__ == '__main__':
    # Create the notes table if it doesn't exist
    db = get_db()
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
    db.close()

    app.run()
