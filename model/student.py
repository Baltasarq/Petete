# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Alumno


from Petete.model.entity import Entity


class Student(Entity):
    def __init__(self,
                 user_id: str,
                 surname: str,
                 name: str,
                 email: str,
                 course: int):
        self._user_id = user_id
        self._surname = surname
        self._name = name
        self._email = email
        self._course = course
        self._project_ids = []

    @property
    def user_id(self):
        return self._user_id

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def name(self) -> str:
        return self._name

    @property
    def complete_name(self) -> str:
        return self.surname + ", " + self.name

    @property
    def email(self) -> str:
        return self._email

    @property
    def course(self):
        return self._course

    def formatted_course(self):
        course = self.course
        return f"{course:4d}/{(course + 1) % 1000:02d}"

    def replace_project_ids(self, lpids: list[str]):
        self._project_ids = list(lpids)

    def add_project_id(self, id: str):
        self._project_ids.append(id)
        
    def delete_project_id(self, id: str):
        self._project_ids.remove(id)

    def remove_project_id(self, id: str):
        self._project_ids.remove(id)

    def all_project_ids(self):
        return list(self._project_ids)

    @property
    def num_projects(self):
        return len(self._project_ids)

    def __str__(self):
        return f"{self.surname} {self.name} ({self.email})"
