# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# User


from typing import Self
import flask_login
import sirope
import werkzeug.security as safe

from Petete.model.entity import Entity


class User(flask_login.UserMixin, Entity):
    def __init__(self, email: str, password: str):
        self._email = email
        self._password = safe.generate_password_hash(password)
        
    @property
    def email(self) -> str:
        return self._email
    
    def get_id(self) -> str:
        return self.email
    
    def chk_password(self, pswd: str) -> bool:
        return safe.check_password_hash(self._password, pswd)

    @staticmethod
    def current_user() -> Self:
        usr = flask_login.current_user
        
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
            
        return usr
    
    @staticmethod
    def find(srp: sirope.Sirope, email: str) -> Self:
        return srp.find_first(User, lambda u: u.email == email)
