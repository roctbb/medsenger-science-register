from flask import send_file

from .manage import *
from .blueprints import *

app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(projects_blueprint, url_prefix='/api')
app.register_blueprint(submission_blueprint, url_prefix='/api')
app.register_blueprint(medsenger_blueprint, url_prefix='/api')
app.register_blueprint(editor_blueprint, url_prefix='/editor')


@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/index.html'))


@app.route('/<path:path>')
def static_path(path):
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/' + path))
