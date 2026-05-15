# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Students module


import flask
import flask_login

from Petete.extensions import srp
from Petete.extensions import crea_basic_sust
from Petete.extensions import retrieve_object_from_request_args
from Petete.model.student import Student
from Petete.model.user import User
from Petete.model.entity import Entity


def crea_students_blprnt():
    blprnt = flask.blueprints.Blueprint(
                                    "students",
                                    __name__,
                                    url_prefix="/students",
                                    template_folder="templates",
                                    static_folder="static")
    return blprnt


url_blprnt_base = lambda: flask.url_for(".list_all")
students_blprnt = crea_students_blprnt()


@students_blprnt.route("/list_all")
@flask_login.login_required
def list_all():
    sust = crea_basic_sust()
    usr = User.current_user()
    sust["students"] = sorted(
                        srp.filter(Student, lambda st: st.user_id == usr.safe_id),
                        key=lambda st: st.complete_name)
    return flask.render_template("students.html", **sust)


@students_blprnt.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add():
    if flask.request.method == "GET":
        return flask.render_template("add_student.html", **crea_basic_sust())

    email = flask.request.form.get("edEmail", "").strip()
    surname = flask.request.form.get("edSurname", "").strip()
    name = flask.request.form.get("edName", "").strip()
    course = int(flask.request.form.get("edCourse", "2000").strip())

    if not email or not surname or not name:
        flask.flash("Datos insuficientes para crear un nuevo estudiante.")
        return flask.redirect(url_blprnt_base())

    usr = User.current_user()

    if srp.find_first(Student, lambda st: st.email == email):
        flask.flash("¡Ese estudiante ya existe!")
        return flask.redirect(url_blprnt_base())

    student = Student(usr.safe_id, surname, name, email, course)
    student.save(srp)
    return flask.redirect(url_blprnt_base())


@students_blprnt.route("/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit():
    if flask.request.method == "GET":
        student, error_msg = retrieve_object_from_request_args()

        if not student:
            flask.flash(error_msg)
            return flask.redirect(url_blprnt_base())

        susts = crea_basic_sust()
        susts |= {
            "student": student
        }

        return flask.render_template("edit_student.html", **susts)
    ...

    student, error_msg = retrieve_object_from_request_args()

    if not student:
        flask.flash(error_msg)
        return flask.redirect(url_blprnt_base())

    surname = flask.request.form.get("edSurname", "").strip()
    name = flask.request.form.get("edName", "").strip()
    email = flask.request.form.get("edEmail", "").strip()
    course = int(flask.request.form.get("edCourse", "2000").strip())

    if not surname or not name or not email:
        flask.flash("datos insuficientes para nuevo estudiante")
        return flask.redirect(url_blprnt_base())

    usr = User.current_user()
    students_with_that_email = srp.filter(
                                    Student,
                                    lambda st: st.email == email
                                            and st.user_id == usr.safe_id)
    students_with_that_email = [st for st
                                in students_with_that_email
                                if st.safe_id != student.safe_id]
    if students_with_that_email:
        flask.flash("La modificación hace que el email coincida con otro estudiante.")
        return flask.redirect(url_blprnt_base())

    new_student = Student(student.user_id, surname, name, email, course)
    new_student.safe_id = student.safe_id
    new_student.__oid__ = student.__oid__
    new_student.replace_project_ids(student.all_project_ids())
    new_student.save(srp)
    return flask.redirect(url_blprnt_base())


@students_blprnt.route("/delete", methods=["GET", "POST"])
@flask_login.login_required
def delete():
    def build_explanation_for(student: Student):
        num_projects = student.num_projects
        toret = "Su información personal será eliminada"

        if num_projects == 1:
            toret += ", así como su único proyecto"
        elif num_projects > 1:
            toret += f", así como sus {num_projects} proyectos"

        return toret + "."
    ...

    if flask.request.method == "GET":
        student, error_msg = retrieve_object_from_request_args()

        if not student:
            flask.flash(error_msg)
            return flask.redirect(url_blprnt_base())

        explain = build_explanation_for(student)
        susts = crea_basic_sust()
        susts |= {
            "msg": f"¿Realmente desea borrar a {student.complete_name}?",
            "explain": build_explanation_for(student),
            "action": "Borrar",
            "cancel": "Volver",
            "action_url": flask.url_for(".delete_student", id=student.safe_id),
            "cancel_url": url_blprnt_base(),

        }

        return flask.render_template("you_sure.html", **susts)
    ...

    student, error_msg = retrieve_object_from_request_args()

    if not student:
        flask.flash(error_msg)
        return flask.redirect(url_blprnt_base())

    # Delete projects
    project_safe_ids = student.all_project_ids()
    project_oids = [srp.oid_from_safe_oid(x) for x in project_safe_ids]
    srp.multi_delete(project_oids)

    # Delete the student
    srp.delete(student.__oid__)
    return flask.redirect(url_blprnt_base())


@students_blprnt.route("/see_student")
@flask_login.login_required
def see():
    student, error_msg = retrieve_object_from_request_args()

    if not student:
        flask.flash(error_msg)
        return flask.redirect(url_blprnt_base())

    project_safe_oids = [srp.oid_from_safe(pid)
                             for pid in student.all_project_ids()]
    sust = crea_basic_sust()
    sust |= {
        "student": student,
        "student_projects": list(srp.multi_load(project_safe_oids))
    }

    return flask.render_template("see_student.html", **sust)


@students_blprnt.route("/list_projects")
@flask_login.login_required
def list_projects():
    student, error_msg = retrieve_object_from_request_args()

    if not student:
        flask.flash(error_msg)
        return flask.redirect(url_blprnt_base())

    projects = srp.multi_load(student.all_project_ids)
    sust = crea_basic_sust()
    sust |= {
        "student": student,
        "projects": projects
    }

    return flask.render_template("projects_for_student.html", **sust)


@students_blprnt.route("/delete_students_of_course", methods=["GET", "POST"])
@flask_login.login_required
def delete_students_of_course():
    if flask.request.method == "GET":
        susts = crea_basic_sust()
        return flask.render_template(flask.url_for("delete_students_of_course.html"))
    ...

    course = int(flask.request.form.get("edCourse", "0").strip())
    students_of_course = srp.filter(Student, lambda st: st.course == course)
    oid_students_of_course = [st.__oid__ for st in students_of_course]
    srp.multi_delete(oid_students_of_course)
