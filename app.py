# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# App Web Flask for the student's project qualification


import flask
import flask_login
import json
import sirope
from datetime import datetime

from Petete.extensions import login_manager
from Petete.extensions import crea_basic_sust
import Petete.views.users.users as users
import Petete.views.projects.projects as projects
import Petete.views.students.students as students
import Petete.views.marks.marks as marks
from Petete.model.user import User
from Petete.model.appinfo import AppInfo


def crea_app():
    app = flask.Flask(__name__)

    app.config.from_file("app.cfg.json", load=json.load)
    lmanager = login_manager
    lmanager.init_app(app)
    app.register_blueprint(users.users_blprnt)
    app.register_blueprint(projects.prjs_blprnt)
    app.register_blueprint(students.students_blprnt)
    app.register_blueprint(marks.marks_blprnt)
    return app


app = crea_app()


@app.route("/")
def index():
    return flask.render_template("index.html", **crea_basic_sust())


if __name__ == "__main__":
    app.run(debug=True)
