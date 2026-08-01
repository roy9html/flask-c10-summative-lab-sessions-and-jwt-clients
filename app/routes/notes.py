from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Note
from app.schemas import NoteSchema
from marshmallow import ValidationError

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Note.query.filter_by(user_id=current_user_id).order_by(Note.created_at.desc())
        paginated_notes = query.paginate(page=page, per_page=per_page, error_out=False)
        
        notes_schema = NoteSchema(many=True)
        notes_data = notes_schema.dump(paginated_notes.items)
        
        return jsonify({
            'notes': notes_data,
            'pagination': {
                'page': paginated_notes.page,
                'per_page': paginated_notes.per_page,
                'total': paginated_notes.total,
                'pages': paginated_notes.pages,
                'has_prev': paginated_notes.has_prev,
                'has_next': paginated_notes.has_next
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        note_schema = NoteSchema()
        validated_data = note_schema.load(data)
        
        note = Note(
            title=validated_data['title'],
            content=validated_data['content'],
            category=validated_data.get('category', 'General'),
            is_archived=validated_data.get('is_archived', False),
            user_id=current_user_id
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify(note_schema.dump(note)), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    try:
        current_user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        note_schema = NoteSchema()
        return jsonify(note_schema.dump(note)), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    try:
        current_user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json()
        note_schema = NoteSchema(partial=True)
        validated_data = note_schema.load(data)
        
        for key, value in validated_data.items():
            setattr(note, key, value)
        
        db.session.commit()
        
        return jsonify(note_schema.dump(note)), 200
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    try:
        current_user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({'message': 'Note deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/notes/archive/<int:note_id>', methods=['PUT'])
@jwt_required()
def archive_note(note_id):
    try:
        current_user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        note.is_archived = not note.is_archived
        db.session.commit()
        
        note_schema = NoteSchema()
        return jsonify(note_schema.dump(note)), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/notes/categories', methods=['GET'])
@jwt_required()
def get_categories():
    try:
        current_user_id = get_jwt_identity()
        categories = db.session.query(Note.category).filter_by(user_id=current_user_id).distinct().all()
        
        return jsonify({
            'categories': [cat[0] for cat in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
