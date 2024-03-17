class Task:
    def __init__(self, title, description, due_date, completed=False, priority=0):
        self._title = title
        self._description = description
        self._due_date = due_date
        self._completed = completed
        self._priority = priority

    def get_title(self):
        return self._title
    
    def set_title(self, title):
        self._title = title

    def get_description(self):
        return self._description
    
    def set_description(self, description):
        self._description = description

    def get_due_date(self):
        return self._due_date
    
    def set_due_date(self, due_date):
        self._due_date = due_date

    def get_completed(self):
        return self._completed
    
    def set_completed(self, completed):
        self._completed = completed

    def get_priority(self):
        return self._priority
    
    def set_priority(self, priority):
        self._priority = priority

    def to_dict(self):
        return {
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "completed": self._completed,
            "priority": self._priority
        }
    