from .manage import *
from .blueprints import *

app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(projects_blueprint, url_prefix='/api')
app.register_blueprint(submission_blueprint, url_prefix='/api')
