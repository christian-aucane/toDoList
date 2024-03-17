from time import strptime
import tkinter as tk
from tkinter import ttk, filedialog

from task_manager import TaskManager

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        try:
            self.task_manager.load()
        except FileNotFoundError:
            pass
        self.title("TODO List")

        self.setup_ui()
        
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.refresh_tasks_tree()

    def verify_date_format(self, date):
        try:
            strptime(date, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def show_modal_window(self, title, message):
        modal_window = tk.Toplevel()
        modal_window.title(title)

        label_message = tk.Label(modal_window, text=message, padx=20, pady=20)
        label_message.pack()

        btn_ok = tk.Button(modal_window, text="OK", command=modal_window.destroy)
        btn_ok.pack()

    def setup_ui(self):
        self.show_modal_window("Bienvenue", "Double clic gauche pour changer le status terminé d'une tâche, Double clic droit pour supprimer une tâche")

        self.lbl_title = tk.Label(self, text="Titre")

        self.entry_title = tk.Entry()
        self.lbl_description = tk.Label(self, text="Description")
        self.entry_description = tk.Entry()
        self.lbl_due_date = tk.Label(self, text="Date d'écheance (JJ/MM/AAAA)")
        self.entry_due_date = tk.Entry()
        self.lbl_priority = tk.Label(self, text="Priorité (0, 1 ou 2 - bassse, moyennne, haute)")
        self.entry_priority = tk.Entry()

        self.btn_add = tk.Button(self, text="Ajouter", command=self.add_task)

        self.lbl_filters = tk.Label(self, text="Filtrer par priorité")
        filters = ["Toutes", "Priorité 0", "Priorité 1", "Priorité 2"]
        self.select_filters = tk.StringVar(self)
        self.select_filters.set("Toutes")
        self.dropdown_filters = tk.OptionMenu(self, self.select_filters, *filters, command=self.on_select_filter)
        
        self.tree = ttk.Treeview(self)

        self.tree["columns"] = ("title", "description", "due_date", "priority", "completed")
        self.tree.column("#0", width=20)
        self.tree.column("title", width=100)  # Colonne du Nom
        self.tree.column("description", width=150)  # Colonne de l'Âge
        self.tree.column("due_date", width=100)
        self.tree.column("completed", width=50)
        self.tree.column("priority", width=50)

        self.tree.heading("#0", text="ID")
        self.tree.heading("title", text="Titre")
        self.tree.heading("description", text="Description")
        self.tree.heading("due_date", text="Date d'échéance")
        self.tree.heading("completed", text="Terminée")
        self.tree.heading("priority", text="Priorité")

        self.btn_export_to_csv = tk.Button(self, text="Exporter en CSV", command=self.export_to_csv)

        self.lbl_title.grid(row=0, column=0)
        self.entry_title.grid(row=0, column=1)
        self.lbl_description.grid(row=1, column=0)
        self.entry_description.grid(row=1, column=1)
        self.lbl_due_date.grid(row=2, column=0)
        self.entry_due_date.grid(row=2, column=1)
        self.lbl_priority.grid(row=3, column=0)
        self.entry_priority.grid(row=3, column=1)
        self.btn_add.grid(row=4, column=0, columnspan=2)
        self.lbl_filters.grid(row=5, column=0)
        self.dropdown_filters.grid(row=5, column=1)
        self.tree.grid(row=6, column=0, columnspan=2)

        self.btn_export_to_csv.grid(row=7, column=0, columnspan=2)

    def refresh_tasks_tree(self, priority=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        tasks = self.task_manager.filter_tasks_by_priority(int(priority)) if priority is not None else self.task_manager.get_tasks()

        for task in tasks:
            title = task.get_title()
            description = task.get_description()
            due_date = task.get_due_date()
            priority = task.get_priority()
            completed = "✔️" if task.get_completed() else "❌"
            self.tree.insert("", "end", values=(title, description, due_date, priority, completed))

        self.tree.bind("<Double-1>", self.on_double_click_left)
        self.tree.bind("<Double-3>", self.on_double_click_right)

    def on_double_click_right(self, event):
        item = self.tree.selection()[0]
        task = self.get_task_from_item(item)
        self.delete_task(task)

    def on_double_click_left(self, event):
        item = self.tree.selection()
        task = self.get_task_from_item(item)
        self.toggle_completed(task)

    def get_task_from_item(self, item):
        title = self.tree.item(item, "values")[0]
        for task in self.task_manager.get_tasks():
            if task.get_title() == title:
                return task
            
    def toggle_completed(self, task):
        task.set_completed(not task.get_completed())
        self.refresh_tasks_tree()

    def delete_task(self, task):
        self.task_manager.delete_task(task)
        self.refresh_tasks_tree()

    def add_task(self):
        title = self.entry_title.get()
        if not title:
            self.show_modal_window("Pas de titre", "Veuillez entrer un titre")
            return
        description = self.entry_description.get()
        if not description:
            self.show_modal_window("Pas de description description", "Veuillez entrer une description")
            return
        due_date = self.entry_due_date.get()
        if not due_date:
            self.show_modal_window("Pas de date d'échéance", "Veuillez entrer une date d'échéance")
            return
        elif not self.verify_date_format(due_date):
            self.show_modal_window("Date d'&échéance invalide", "Veuillez entrer un format de date valide 'DD/MM/YYYY'")
            return
        priority = self.entry_priority.get()
        if not priority:
            self.show_modal_window("Pas de priorité", "Veuillez entrer une priorité")
            return
        elif priority not in ["0", "1", "2"]:
            self.show_modal_window("Priorité invalide", "Veuillez entrer une priorité comprise entre 0 and 2")
            return
        self.task_manager.add(title, description, due_date, int(priority))
        self.refresh_tasks_tree()

    def export_to_csv(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.task_manager.export_to_csv(file_path)
                tk.messagebox.showinfo("Export Réussis", "La TODO liste a été exporté avec succès a l'emplacement suivant : " + file_path)
            else:
                tk.messagebox.showwarning("Export Echoué", "Aucun fichier sélectionné pour l'exportation")

    def on_select_filter(self, value):
        if value == "Toutes":
            self.refresh_tasks_tree()
        else:
            self.refresh_tasks_tree(value.split(" ")[-1])

    def quit(self):
        self.task_manager.save()
        self.destroy()

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()