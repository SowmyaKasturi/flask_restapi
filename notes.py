from flask import abort, make_response
from config import db
from models import Note, Person, note_schema


def create(note):
    person_id = note.get("person_id")
    person = Person.query.get(person_id)
    if person:
        new_note = note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(404, "Note with id {} not found".format(person_id))

def read_one(note_id):
    note = Note.query.get(note_id)
    if note is not None:
        return note_schema.dump(note)
    else:
        abort(404, "Note with id {} not found".format(note_id))

def update(note_id, note):
    existing_note = Note.query.get(note_id)
    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()
        return note_schema.dump(existing_note), 201
    else:
        abort(404, "Note with id {} not found".format(note_id))

def delete(note_id):
    existing_note = Note.query.get(note_id)
    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response("{} note id successfully deleted".format(note_id))
    else:
        abort(404, "Note with id {} not found".format(note_id))