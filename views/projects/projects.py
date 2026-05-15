# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Projects module


import flask
import flask_login

from Petete.model.user import User
from Petete.model.entity import Entity
from Petete.model.project import Project

from Petete.extensions import login_manager
from Petete.extensions import crea_basic_sust
from Petete.extensions import retrieve_object_from_request_args
from Petete.extensions import srp


def crea_projects_blprnt():
    blprnt = flask.blueprints.Blueprint(
                                    "projects",
                                    __name__,
                                    url_prefix="/projects",
                                    template_folder="templates",
                                    static_folder="static")
    return blprnt


prjs_blprnt = crea_projects_blprnt()


@prjs_blprnt.route("/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit():
    if flask.request.method == "GET":
        susts = crea_basic_sust()
        project, error_msg = retrieve_object_from_request_args()
        
        if not project:
            flask.flash(error_msg)
            return flask.redirect(flask.url_for("students.list_all"))
        
        student = Entity.load_from_safe_oid(srp, project.student_id)
        
        susts |= {
            "project": project,
            "student": student,
        }
        return flask.render_template("edit_project.html", **susts)
    ...
    
    title = flask.request.form.get("edTitle", "")
    notes = flask.request.form.get("edNotes", "")
    
    if not title:
        flask.flash("Se necesita un título para el proyecto.")
        return flask.redirect(flask.url_for("students.see"))
    
    usr = User.current_user()
    project, error_msg = retrieve_object_from_request_args()
    
    if not project:
        flask.flash(error_msg)
        return flask.redirect(flask.url_for("students.list_all"))
    
    new_project = Project(
                        usr.safe_id,
                        project.student_id,
                        title,
                        notes,
                        marks)
    
    new_project.safe_id = project.safe_id
    new_project.__oid__ = project.__oid__
    new_project.save(srp)
    return flask.redirect(flask.url_for("students.see", id=project.student_id))
    
    
@prjs_blprnt.route("/delete", methods=["GET", "POST"])
@flask_login.login_required
def delete():
    if flask.request.method == "GET":
        project, error_msg = retrieve_object_from_request_args()

        if not project:
            flask.flash(error_msg)
            return flask.redirect(flask.url_for("students.list_all"))

        susts = crea_basic_sust()
        susts |= {
            "msg": f"¿Realmente desea borrar '{project.title}'?",
            "explain": "Esta acción no puede deshacerse.",
            "action": "Borrar",
            "cancel": "Volver",
            "action_url": flask.url_for(".delete_project", id=project.safe_id),
            "cancel_url": flask.url_for("students.see", id=project.student_id),

        }

        return flask.render_template("you_sure.html", **susts)
    ...

    project, error_msg = retrieve_object_from_request_args()

    if not project:
        flask.flash(error_msg)
        return flask.redirect("students.list_all")

    student = Entity.load_from_safe_oid(srp, project.student_id)
    student.delete_project_id(project.safe_id)
    student.save(srp)
    srp.delete(project.__oid__)
    return flask.redirect(flask.url_for("students.see", id=student.safe_id))


@prjs_blprnt.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add():
    if flask.request.method == "GET":
        student, error_msg = retrieve_object_from_request_args()
        
        if not student:
            flask.flash(error_msg)
            return flask.redirect(flask.url_for("students.list_all"))

        susts = crea_basic_sust()
        susts |= {
            "student": student,
        }

        return flask.render_template("add_project.html", **susts)
    ...
    
    title = flask.request.form.get("edTitle", "")
    notes = flask.request.form.get("edNotes", "")
    
    if not title:
        flask.flash("Se necesita un título para el proyecto.")
        return flask.redirect(flask.url_for("students.see"))
    
    student, error_msg = retrieve_object_from_request_args()
    
    if not student:
        flask.flash(error_msg)
        return flask.redirect(flask.url_for("students.list_all"))
        
    usr = User.current_user()    
    project = Project(usr.safe_id, student.safe_id, title, notes)
    project.save(srp)
    student.add_project_id(project.safe_id)
    student.save(srp)
    return flask.redirect(flask.url_for("students.see", id=student.safe_id))


@prjs_blprnt.route("/see")
@flask_login.login_required
def see():
    project, error_msg = retrieve_object_from_request_args()
    
    if not project:
        flask.flash(error_msg)
        return flask.redirect(flask.url_for("students.list_all"))
    
    student = Entity.load_from_safe_oid(srp, project.student_id)
    susts = crea_basic_sust()
    susts |= {
        "project": project,
        "student": student,
        "months": [m.name for m in list(Project.Month)]
    }
    
    return flask.render_template("see_project.html", **susts)
