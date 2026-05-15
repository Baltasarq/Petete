# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Extensions


import flask
import flask_login
import sirope

from Petete.model.user import User
from Petete.model.student import Student
from Petete.model.appinfo import AppInfo
from Petete.model.entity import Entity


login_manager = flask_login.login_manager.LoginManager()
srp = sirope.Sirope()


def crea_basic_sust() -> dict[str, str]:
    """Crea las sustituciones básicas para todas las plantillas.
        :return: un diccionario texto clave -> a texti valor.
    """
    return {
        "AppInfo": AppInfo,
        "usr": User.current_user()
    }


def retrieve_object_from_request_args(arg_name="id"):
    object_id = flask.request.args.get(arg_name)

    if not object_id:
        return None, "se necesita un id para recuperar un objeto"

    toret = Entity.load_from_safe_oid(srp, object_id)

    if not toret:
        return None, "el id proporcionado no se corresponde con ningún objeto"

    return toret, "Ok"
