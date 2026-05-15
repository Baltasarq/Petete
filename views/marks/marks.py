# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Marks module


import flask
import flask_login
from datetime import datetime

from Petete.model.user import User
from Petete.model.entity import Entity
from Petete.model.project import Project

from Petete.extensions import login_manager
from Petete.extensions import crea_basic_sust
from Petete.extensions import retrieve_object_from_request_args
from Petete.extensions import srp


def crea_marks_blprnt():
    blprnt = flask.blueprints.Blueprint(
                                    "marks",
                                    __name__,
                                    url_prefix="/marks",
                                    template_folder="templates")
    return blprnt


marks_blprnt = crea_marks_blprnt()
get_url_students_list_all = lambda: flask.url_for("students.list_all")
get_url_projects_see_for = lambda id: flask.url_for("projects.see", id=id)


@marks_blprnt.route("/add", methods=["GET", "POST"])
@flask_login.login_required
def add():
    if flask.request.method == "GET":
        project, error_msg = retrieve_object_from_request_args()
        
        if not project:
            flask.flash(error_msg)
            return flask.redirect(get_url_students_list_all_url())
        
        susts = crea_basic_sust()
        susts |= {
            "Months": Project.Month,
            "project": project
        }
        
        return flask.render_template("add_mark.html", **susts)
    ...

    dt = datetime.now()
    str_year = flask.request.form.get("edYear", str(dt.year))
    str_month = flask.request.form.get("edMonth", Project.Month.SEP.name)
    str_mark = flask.request.form.get("edMark", "0")
    
    year = int(str_year)
    month = Project.Month[str_month]
    project, error_msg = retrieve_object_from_request_args()
    
    if not project:
        flask.flash(error_msg)
        return flask.redirect(get_url_students_list_all_url())
    
    mark = project.find_mark_for_month(year, month)
    
    if mark:
        flask.flash(f"Ya hay una calificación para {year:04d}/{month.name}")
        return flask.redirect(get_url_projects_see_for(project.safe_id))
    
    project.add_mark(year, month, float(str_mark))    
    project.save(srp)
    return flask.redirect(get_url_projects_see_for(project.safe_id))


@marks_blprnt.route("/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit():
    if flask.request.method == "GET":
        project, error_msg = retrieve_object_from_request_args()
        
        if not project:
            flask.flash(error_msg)
            return flask.redirect(get_url_students_list_all())
        
        str_year = flask.request.args.get("year", "2020")
        arg_month = flask.request.args.get("month", Project.Month.SEP.name)
        
        if isinstance(arg_month, str):
            month = Project.Month[arg_month]
        else:
            month = arg_month
        
        year = int(str_year)
        mark = project.find_mark_for_month(year, month)
        
        if not mark:
            flask.flash(f"there is no mark for month '{month.name}'")
            return flask.redirect(get_url_projects_see_for(project.safe_id))
        
        susts = crea_basic_sust()
        susts |= {
            "Months": Project.Month,
            "project": project,
            "mark": mark,
            "str_mark": Project.str_from_mark(mark),
        }
        return flask.render_template("edit_mark.html", **susts)
    ...
    project, error_msg = retrieve_object_from_request_args()
        
    if not project:
        flask.flash(error_msg)
        return flask.redirect(get_url_students_list_all())
    
    str_year = flask.request.args.get("year", "2020")
    arg_month = flask.request.args.get("month", Project.Month.SEP.name)
    str_mark_value = flask.request.form.get("edMark", "0")
    month = Project.Month[arg_month]    
    year = int(str_year)
    mark = project.find_mark_for_month(year, month)
    
    if not mark:
        flask.flash(f"there is no mark for month '{month.name}'")
        return flask.redirect(get_url_projects_see_for(project.safe_id))

    mark[2] = float(str_mark_value)
    project.modify_mark(mark)
    project.save(srp)
    return flask.redirect(get_url_projects_see_for(project.safe_id))


@marks_blprnt.route("/delete")
@flask_login.login_required
def delete():
    project, error_msg = retrieve_object_from_request_args()
    
    if not project:
        flask.flash(error_msg)
        return flask.redirect(get_url_students_list_all())
    
    str_year = flask.request.args.get("year", "2020")
    str_month = flask.request.args.get("month", Project.Month.SEP.name)
    month = Project.Month[str_month]
    year = int(str_year)
    mark = project.find_mark_for_month(year, month)
    
    if not mark:
        flask.flash(f"there is no mark for month {year:04d}/{month.name}")
        return flask.redirect(get_url_projects_see_for(project.safe_id))
    
    project.delete_mark(year, month)
    project.save(srp)
    return flask.redirect(get_url_projects_see_for(project.safe_id))


@marks_blprnt.route("/delete_all")
@flask_login.login_required
def delete_all():
    project, error_msg = retrieve_object_from_request_args()
    
    if not project:
        flask.flash(error_msg)
        return flask.redirect(get_url_students_list_all())
    
    project.delete_all_marks()
    project.save(srp)    
    return flask.redirect(get_url_projects_see_for(project.safe_id))
