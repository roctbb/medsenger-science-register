from flask import Blueprint, request, render_template, redirect, send_file
from backend.methods import *
from backend.models import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from backend.config import *

editor_blueprint = Blueprint('editor', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == EDITOR_USERNAME and check_password_hash(EDITOR_PASSWORD_HASH, password):
        return username


@editor_blueprint.route('/', methods=['get'])
@auth.login_required
def get_form_parts():
    form_parts = FormPart.query.all()

    return render_template('form_parts.html', parts=form_parts)


@editor_blueprint.route('/create', methods=['get'])
@auth.login_required
def create_part_page():
    return render_template('questionnaire.html')


@editor_blueprint.route('/full_report/<project_id>', methods=['get'])
@auth.login_required
def full_report_page(project_id):
    project = Project.query.get_or_404(project_id)

    filename = save_to_excel(generate_report_for_project(project))

    return send_file(filename)

    #return render_template('project_report.html', reports=generate_report_for_project(project))


@editor_blueprint.route('/create', methods=['post'])
@auth.login_required
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


@editor_blueprint.route('/parts/<int:part_id>', methods=['get'])
@auth.login_required
def edit_part_page(part_id):
    form_part = FormPart.query.get(part_id)

    return render_template('questionnaire.html', form_json=json.dumps(form_part.as_dict()))


@editor_blueprint.route('/parts/<int:part_id>', methods=['post'])
@auth.login_required
def update_and_save_part_page(part_id):
    data = request.json
    form_part = FormPart.query.get(part_id)
    form_part.name = data.get('name')
    form_part.description = data.get('description')
    form_part.repeatable = data.get('repeatable')
    form_part.fields = data.get('fields')
    db.session.commit()

    return jsonify({
        "state": "ok",
        "id": form_part.id,
        "name": form_part.name
    })


@editor_blueprint.route("/delete/<int:part_id>", methods=["delete"])
@auth.login_required
def delete_part_page(part_id):
    form_part = FormPart.query.get(part_id)
    db.session.delete(form_part)
    db.session.commit()

    return jsonify({
        "state": "ok"
    })
