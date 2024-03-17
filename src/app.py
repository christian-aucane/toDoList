from task_manager import TaskManager
from time import strptime

class TodoListApp:
    def __init__(self):
        self.task_manager = TaskManager()
        try:
            print("Chargement des taches ...")
            self.task_manager.load()
            print("Tâches chargeées")
        except FileNotFoundError:
            print("Pas de taches trouvées ...")
            pass
        self.prompt = "Que souhaitez-vous faire ?\n1. Ajouter une tâche\n2. Supprimer une tâche\n3. Afficher les tâches\n4. Filtrer les taches par priorité\n5. Quitter"
        self.main_loop = True

    def add_task(self):
        print("Ajouter une tâche\n")
        title = input("Titre : ")
        description = input("Description : ")
        while True:
            try:
                due_date = input("Date d'écheance (JJ/MM/AAAA): ")
                due_date = strptime(due_date, "%d/%m/%Y")
                break
            except ValueError:
                print("Date invalide")
        while True:
            try:
                priority = int(input("Priorité (0, 1 ou 2 - bassse, moyennne, haute): "))
                if priority < 0 or priority > 2:
                    raise ValueError
                break
            except ValueError:
                print("Priorité invalide")

        self.task_manager.add(title, description, due_date, priority=priority)
        self.task_manager.sort_tasks_by_priority()

        print("Tâche ajoutée")

    def remove_task(self):
        print("Supprimer une tâche\n")
        while True:
            try:
                i = int(input("Quelle tâche souhaitez-vous supprimer (numéro) ? "))
                self.task_manager.delete(i - 1)  # -1 car la liste commence a 0
                break
            except IndexError:
                print("Tâche introuvable")

    def show_tasks(self):
        print("Afficher les tâches\n")
        self.task_manager.show()

    def show_filtered_tasks(self):
        print("Afficher les tâches par priorité\n")
        while True:
            try:
                priority = int(input("Priorité (0, 1 ou 2 - bassse, moyennne, haute): "))
                if priority not in [0, 1, 2]:
                    raise ValueError
                break
            except ValueError:
                print("Priorité invalide")
        self.task_manager.show_tasks_by_priority(priority)

    def quit(self):
        self.main_loop = False
        print("Sauvegarde des tâches ...")
        self.task_manager.save()
        
        print("Merci d'avoir utilisé notre application !")

    def run(self):
        while self.main_loop:
            print(self.prompt)
            choice = input("Votre choix : ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.remove_task()
            elif choice == "3":
                self.show_tasks()
            elif choice == "4":
                self.show_filtered_tasks()
            elif choice == "5":
                self.quit()
            else:
                print("Choix invalide. Veuillez reessayer.")


if __name__ == "__main__":
    app = TodoListApp()
    app.run()
