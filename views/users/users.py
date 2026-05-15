# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Users module


import flask
import flask_login
from Petete.model.user import User
from Petete.extensions import login_manager
from Petete.extensions import crea_basic_sust
from Petete.extensions import srp


def crea_users_blprnt():
    blprnt = flask.blueprints.Blueprint(
                                    "users",
                                    __name__,
                                    url_prefix="/users",
                                    template_folder="templates")
    return blprnt, login_manager


users_blprnt, lm = crea_users_blprnt()


@lm.user_loader
def user_loader(name):
    return User.find(srp, name)


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Usuario no autorizado")
    return flask.redirect(flask.url_for("index"))


@users_blprnt.route("/login", methods=["POST"])
def login():
    email = flask.request.form.get("edEmail")
    password = flask.request.form.get("edPassword")

    if not email or not password:
        flask.flash("Es necesario un e.mail de usuario y su contraseña")
        return flask.redirect(flask.url_for("index"))

    usr = User.find(srp, email)

    if not usr:
        flask.flash("No existe un usuario con ese e.mail")
        return flask.redirect(flask.url_for("index"))

    if not usr.chk_password(password):
        flask.flash("Contraseña incorrecta para: " + email)
        return flask.redirect(flask.url_for("index"))

    flask_login.login_user(usr)
    return flask.redirect(flask.url_for("students.list_all"))


@users_blprnt.route("/add", methods=["GET", "POST"])
def add():
    if flask.request.method == "GET":
        return flask.render_template("add_user.html", **crea_basic_sust())

    email = flask.request.form.get("edEmail")
    password = flask.request.form.get("edPassword")

    if not email or not password:
        flask.flash("Es necesario un e.mail de usuario y su contraseña")
        return flask.redirect(flask.url_for(".add"))

    usr = User.find(srp, email)

    if usr:
        flask.flash("Ya hay un usuario con ese e.mail en el sistema.")
        return flask.redirect(flask.url_for("index"))

    usr = User(email, password)
    usr.save(srp)
    flask.flash("¡Ahora ya puede hacer login!")
    return flask.redirect(flask.url_for("index"))


@users_blprnt.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))
