from flask import send_file

from .manage import *
from .blueprints import *

app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(projects_blueprint, url_prefix='/api')
app.register_blueprint(comments_blueprint, url_prefix='/api')
app.register_blueprint(submission_blueprint, url_prefix='/api')
app.register_blueprint(medsenger_blueprint, url_prefix='/api')
app.register_blueprint(file_blueprint, url_prefix='/api')
app.register_blueprint(editor_blueprint, url_prefix='/editor')
app.register_blueprint(account_blueprint, url_prefix='/')


@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/index.html'))

@app.route('/favicon.ico')
def favicon():
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/favicon.ico'))

@app.route('/css/<path:path>')
def css(path):
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/css/' + path))

@app.route('/ico/<path:path>')
def ico(path):
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/ico/' + path))

@app.route('/js/<path:path>')
def js(path):
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/js/' + path))

@app.route('/images/<path:path>')
def images(path):
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/images/' + path))

@app.route('/img/<path:path>')
def img(path):
    return send_file(os.path.join(os.path.dirname(__file__), '../dist/img/' + path))
