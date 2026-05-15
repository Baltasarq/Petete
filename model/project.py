# Petete (c) Baltasar 2026 MIT License <jbgarcia@uvigo.gal>
# Project


from enum import Enum, auto

from Petete.model.entity import Entity


class Project(Entity):
    class Month(Enum):
        SEP = auto()
        FEB = auto()
        JUN = auto()
        JUL = auto()


    def __init__(self,
                 user_id: str,
                 student_id: str,
                 title: str,
                 notes: str,
                 marks: list[list[int, Project.Month, float]] = None):
        self._user_id = user_id
        self._student_id = student_id
        self._title = title
        self._notes = notes
        self._marks = []
        
        if self.marks:
            for mark in self._marks:
                self.add(mark[0], mark[1], mark[2])
        
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def student_id(self) -> str:
        return self._student_id
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @property
    def all_marks(self) -> list[list[year: int, month: Project.Month, mark: floar]]:
        """Returns all marks as a list of tuples.
            :return: a list of tuples with: year, Project.Month, mark.
        """
        return [list([mark[0], Project.Month(mark[1]), mark[2]])
                       for mark in self._marks]
    
    @property
    def num_marks(self) -> int:
        return len(self._marks)
    
    @property
    def final_mark(self) -> float:
        """The final (last) mark, or None if no mark is found.
            :return: the last mark, or None.
        """
        toret = None
        
        if self._marks:
            toret = self._marks[-1][2]
            
        return toret
    
    def add_mark(self, year: int, month: Project.Month, mark: float):
        self._marks.append(list([year, month.value, mark]))
        
    def delete_all_marks(self):
        self._marks.clear()
        
    def delete_mark(self, year: int, month: Project.Month):
        self._marks = [m for m in self._marks
                           if year != m[0] or month.value != m[1]]
        
    def modify_mark(self, mark: list[int, Project.Month, float]):
        toret = False
        
        print(f"New mark is: {mark[2]}")
        for i, m in enumerate(self._marks):
            if (m[0] == mark[0]
            and m[1] == mark[1].value):
                self._marks[i][2] = mark[2]
                toret = True
                break
            
        return toret
        
    @staticmethod
    def str_from_mark(m: list[int, Project.Month, float]):
        return f"{m[0]:04d}/{Project.Month(m[1]).name}/{m[2]:5.2f}"
    
    def find_mark_for_month(self, year: int, month: Project.Month) -> list[int, Project.Month, float]:
        toret = [mark for mark in self._marks
                         if mark[0] == year and mark[1] == month.value]
        
        if toret:
            toret = list(toret[0])
            toret[1] = Project.Month(toret[1])
        else:
            toret = None
            
        return toret
    
    def __str__(self):
        toret = f"{self.title:25s}/\"{self.notes:20s}\""
        return toret + str.join("\n\t", [Project.str_from_mark(m) for m in self._marks])
