from time import strftime
import json
import csv

from task import Task

class TaskManager:
    def __init__(self):
        self._tasks = []

    def add(self, title, description, due_date, priority=0):
        task = Task(title, description, due_date, priority=priority)
        self._tasks.append(task)

    def delete(self, i):
        try:
            del self._tasks[i]
            return True
        except IndexError:
            return False
    
    def delete_task(self, task):
        try:
            self._tasks.remove(task)
            return True
        except ValueError:
            return False
        
    def show(self):
        if len(self._tasks) == 0:
            print("Aucune tâche ...")
            return
        for task in self._tasks:
            self.show_task(task)

    def get_tasks(self):
        return self._tasks

    def get_task_str(self, task):
        i = self._tasks.index(task) + 1
        title = task.get_title()
        description = task.get_description()
        date = strftime("%d/%m/%Y", task.get_due_date())
        finish = "Oui" if task.get_completed() else "Non"
        priority = task.get_priority()
        return f"{i}. Titre: {title}\nDescription: {description}\nDate d'écheance: {date}\nTerminée: {finish}\nPriorité: {priority}\n"  
    
    def get_tasks_str(self):
        return "\n\n".join(self.get_task_str(task) for task in self._tasks)
    
    def filter_tasks_by_priority_str(self, priority):
        print("Afficher les tâches par priorité\n")
        return "\n\n".join(self.get_task_str(task) for task in self.filter_tasks_by_priority(priority))
    
    def show_task(self, task):
        print(self.get_task_str(task))

    def get_highest_priority_task(self):
        try:
            max_priority = max(task.priority for task in self._tasks)
            highest_priority_tasks = [task for task in self._tasks if task.priority == max_priority]
            # Return the first task found with the highest priority
            return highest_priority_tasks[0] if highest_priority_tasks else None
        except ValueError:
            return None

    def sort_tasks_by_priority(self):
        self._tasks.sort(key=lambda task: (task.get_priority(), task.get_due_date()), reverse=True)

    def set_task_priority(self, i, priority):
        self._tasks[i].set_priority(priority)

    def filter_tasks_by_priority(self, priority):
        return [task for task in self._tasks if task.get_priority() == priority]
    
    def show_tasks_by_priority(self, priority):
        for task in self.filter_tasks_by_priority(priority):
            self.show_task(task)

    def save(self, path="tasks.json"):
        # TODO : gestion des erreurs
        tasks = [task.to_dict() for task in self._tasks]
        with open(path, "w") as file:
            json.dump(tasks, file, indent=4)
        return True
        
    def load(self, path="tasks.json"):
        with open(path, "r") as file:
            tasks = json.load(file)
            for task in tasks:
                task["due_date"] = tuple(task["due_date"])
                self._tasks.append(Task(**task))

    def delete_json(self, path="tasks.json"):
        with open(path, "w") as file:
            json.dump([], file)
        
    def export_to_csv(self, path="tasks.csv"):
        with open(path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Description", "Due Date", "Completed", "Priority"])
            for task in self._tasks:
                writer.writerow([task.get_title(), task.get_description(), task.get_due_date(), task.get_completed(), task.get_priority()])
    