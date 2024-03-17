import curses
from time import strptime

from task_manager import TaskManager

class TodoListApp:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.prompt = "Que souhaitez-vous faire ?\n1. Ajouter une tâche\n2. Supprimer une tâche\n3. Afficher les tâches\n4. Filtrer les tâches par priorité\n5. Quitter"
        self.main_loop = True
        self.task_manager = TaskManager()

        try:
            self.stdscr.addstr("Chargement des tâches ...")
            self.stdscr.refresh()
            self.task_manager.load()
            self.stdscr.addstr("Taâches chargeées")
            self.stdscr.refresh()
        except FileNotFoundError:
            self.stdscr.addstr("Pas de tâches trouvées")
            self.stdscr.refresh()
            pass

        self.run()

    def run(self):
        while self.main_loop:
            self.stdscr.clear()
            self.stdscr.addstr(self.prompt + "\n")
            self.stdscr.refresh()
            choice = self.stdscr.getch()

            if choice == ord('1'):
                self.add_task()
            elif choice == ord('2'):
                self.remove_task()
            elif choice == ord('3'):
                self.show_tasks()
            elif choice == ord('4'):
                self.show_filtered_tasks()
            elif choice == ord('5'):
                self.quit()
            else:
                self.stdscr.addstr("Choix invalide. Veuillez réessayer.\n")
                self.stdscr.refresh()

    def get_input(self):
        input_text = ''
        while True:
            char = self.stdscr.getch()
            if char == curses.KEY_ENTER or char == 10:
                break
            elif char == curses.KEY_BACKSPACE or char == 127:
                input_text = input_text[:-1]
            else:
                input_text += chr(char)
            self.stdscr.addstr(chr(char))
            self.stdscr.refresh()
        return input_text

    def add_task(self):
        # Code pour ajouter une tâche
        self.stdscr.clear()
        self.stdscr.addstr("Titre : ")
        self.stdscr.refresh()
        title = self.get_input()
        self.stdscr.addstr("\nDescription : ")
        self.stdscr.refresh()
        description = self.get_input()
        while True:
            try:
                self.stdscr.addstr("\nDate d'écheance (JJ/MM/AAAA): ")
                self.stdscr.refresh()
                due_date = self.get_input()
                due_date = strptime(due_date, "%d/%m/%Y")
                break
            except ValueError:
                self.stdscr.addstr("\nDate invalide\n")
                self.stdscr.refresh()
        while True:
            try:
                self.stdscr.addstr("\nPriorité (0, 1 ou 2 - bassse, moyennne, haute): ")
                self.stdscr.refresh()

                priority = int(self.stdscr.getch()) - 48
                self.stdscr.addstr(str(priority))
                if priority not in (0, 1, 2):
                    raise ValueError
                break
            except ValueError:
                self.stdscr.addstr("\nPriorité invalide\n")

        self.task_manager.add(title, description, due_date, priority=priority)
        self.task_manager.sort_tasks_by_priority()

    def remove_task(self):
        # Code pour supprimer une tâche
        self.stdscr.clear()
        self.stdscr.addstr("Quele tache voulez vous supprimer (numéro)?")
        self.stdscr.refresh()
        i = int(self.stdscr.getch()) - 1
        deleted = self.task_manager.delete(i)
        if deleted:
            self.task_manager.sort_tasks_by_priority()
            self.stdscr.addstr("\nTâche supprimée")
            self.stdscr.refresh()
            self.stdscr.getch()
        else:
            self.stdscr.addstr("\nTâche introuvable")

    def show_tasks(self):
        # Code pour afficher les tâches
        self.stdscr.clear()
        self.stdscr.addstr(self.task_manager.get_tasks_str())
        self.stdscr.refresh()
        self.stdscr.getch()

    def show_filtered_tasks(self):
        # Code pour afficher les tâches filtrées par priorité
        
        self.stdscr.clear()
        while True:
            try:
                self.stdscr.addstr("Afficher les tâches par priorité\nQuelle priorité voulez-vous afficher (0, 1 ou 2 - bassse, moyennne, haute)?")
                self.stdscr.refresh()
                priority = self.stdscr.getch() - 48
                if priority not in (0, 1, 2):
                    raise ValueError
                break
            except ValueError:
                self.stdscr.addstr("Priorité invalide\n")
        self.stdscr.clear()
        self.stdscr.addstr(f"Priorité {priority} :\n")
        self.stdscr.addstr(self.task_manager.filter_tasks_by_priority_str(priority))
        self.stdscr.refresh()
        self.stdscr.getch()
       

    def quit(self):
        # Code pour quitter l'application
        self.stdscr.clear()
        self.stdscr.addstr("Sauvegarde des tâches ..\n.")
        self.stdscr.refresh()
        saved = self.task_manager.save()
        if saved:
            self.stdscr.addstr("Tâches sauvegardées\n")
            self.stdscr.refresh()
        else:
            self.stdscr.addstr("Erreur de sauvegarde\n")
            self.stdscr.refresh()

        self.main_loop = False
        self.stdscr.addstr("Merci d'avoir utilisé notre application !\n")
        self.stdscr.refresh()
        self.stdscr.getch()

        
if __name__ == "__main__":
    curses.wrapper(TodoListApp)
