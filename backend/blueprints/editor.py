from flask import Blueprint, request, render_template, redirect
from backend.methods import *
from backend.models import *


editor_blueprint = Blueprint('editor', __name__)


@editor_blueprint.route('/get_data', methods=["get"])
def get_data():
    form_parts = FormPart.query.all()

    return json.dumps(as_dict(form_parts))


@editor_blueprint.route('/', methods=['get'])
def get_form_parts():
    form_parts = FormPart.query.all()

    return render_template('form_parts.html', parts=form_parts)


@editor_blueprint.route('/<int:part_id>', methods=['get'])
def edit_part_page(part_id):
    form_part = FormPart.query.get(part_id)

    return render_template('questionnaire.html', form_json=json.dumps(form_part.as_dict()))


@editor_blueprint.route('/create/', methods=['get'])
def create_part_page():
    return render_template('questionnaire.html')


@editor_blueprint.route('/create/', methods=['post'])
def save_part_page():
    data = request.json
    form_part = FormPart()
    form_part.name = data.get('name')
    form_part.fields = data.get('fields')
    db.session.add(form_part)
    db.session.commit()

    return jsonify({
        "state": "ok",
        "id": form_part.id,
        "name": form_part.name
    })


@editor_blueprint.route('/<int:part_id>', methods=['post'])
def update_and_save_part_page(part_id):
    data = request.json
    form_part = FormPart.query.get(part_id)
    form_part.name = data.get('name')
    form_part.fields = data.get('fields')
    db.session.commit()

    return jsonify({
        "state": "ok",
        "id": form_part.id,
        "name": form_part.name
    })


@editor_blueprint.route("/delete/<int:part_id>", methods=["get"])
def delete_part_page(part_id):
    form_part = FormPart.query.get(part_id)
    db.session.delete(form_part)
    db.session.commit()

    return redirect("/editor")

