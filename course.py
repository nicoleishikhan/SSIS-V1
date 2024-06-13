import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class CourseInformationSystemGUI:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        self.master.title("Course Management System")
        self.master.configure(bg="#f0f4f8")
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_fullscreen)

        self.create_header()
        self.create_form()
        self.create_buttons()
        self.create_treeview()
        self.load_courses()

    def create_header(self):
        header = tk.Label(
            self.master,
            text="COURSE MANAGEMENT SYSTEM",
            font=("Helvetica", 24, "bold"),
            bg="#bbdefb",
            fg="#0d47a1",
            pady=10
        )
        header.pack(side=tk.TOP, fill=tk.X, pady=20)

    def create_form(self):
        self.csv_filename = "courses.csv"
        self.fields = ["Course Code", "Course Title"]
        labels = ["Course Code", "Course Title"]
        self.entries = {}

        form_frame = tk.Frame(self.master, bg="#f0f4f8")
        form_frame.pack(pady=20)

        for idx, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, font=("Helvetica", 14), bg="#f0f4f8", fg="#0d47a1")
            label.grid(row=idx, column=0, padx=10, pady=10, sticky='w')
            entry = tk.Entry(form_frame, font=("Helvetica", 14))
            entry.grid(row=idx, column=1, padx=10, pady=10, sticky='w')
            self.entries[label_text] = entry

    def create_buttons(self):
        button_style = {
            'font': ("Helvetica", 12),
            'bg': "#90caf9",
            'fg': "#0d47a1",
            'relief': tk.FLAT,
            'width': 20,
            'height': 2,
            'bd': 0
        }

        button_frame = tk.Frame(self.master, bg="#f0f4f8")
        button_frame.pack(pady=10)

        add_btn = tk.Button(button_frame, text="Add Course", command=self.add_course, **button_style)
        add_btn.grid(row=0, column=0, padx=10, pady=5)

        edit_btn = tk.Button(button_frame, text="Edit Course", command=self.edit_course, **button_style)
        edit_btn.grid(row=0, column=1, padx=10, pady=5)

        save_btn = tk.Button(button_frame, text="Save Changes", command=self.save_changes, **button_style)
        save_btn.grid(row=1, column=0, padx=10, pady=5)

        delete_btn = tk.Button(button_frame, text="Delete Course", command=self.delete_course, **button_style)
        delete_btn.grid(row=1, column=1, padx=10, pady=5)

        search_label = tk.Label(self.master, text="Search Course:", font=("Helvetica", 14), bg="#f0f4f8", fg="#0d47a1")
        search_label.pack(pady=5)
        self.search_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.search_entry.pack(pady=5)
        search_btn = tk.Button(self.master, text="Search", command=self.search_course, **button_style)
        search_btn.pack(pady=5)

    def create_treeview(self):
        self.tree = ttk.Treeview(self.master, columns=("Course Code", "Course Title"), show="headings")
        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Title", text="Course Title")

        self.tree.column("Course Code", width=150)
        self.tree.column("Course Title", width=300)
        self.tree.pack(pady=20)

    def load_courses(self):
        self.tree.delete(*self.tree.get_children())
        try:
            with open(self.csv_filename, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass

    def add_course(self):
        values = [self.entries[label].get() for label in self.entries]
        if any(not value for value in values):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if self.course_exists(values[0]):
            messagebox.showerror("Error", f"Course {values[0]} already exists.")
            return

        with open(self.csv_filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(values)

        self.tree.insert("", "end", values=values)
        self.clear_entries()
        messagebox.showinfo("Success", "Course added successfully!")

    def edit_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        self.selected_item = selected[0]
        values = self.tree.item(selected, "values")
        for idx, label in enumerate(self.entries):
            self.entries[label].delete(0, tk.END)
            self.entries[label].insert(0, values[idx])

    def save_changes(self):
        if not hasattr(self, 'selected_item'):
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        values = [self.entries[label].get() for label in self.entries]
        self.tree.item(self.selected_item, values=values)

        all_courses = []
        with open(self.csv_filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                all_courses.append(row)

        for row in all_courses:
            if row[0] == self.tree.item(self.selected_item, "values")[0]:
                row[:] = values
                break

        with open(self.csv_filename, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(all_courses)

        self.selected_item = None
        self.clear_entries()

    def delete_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to delete.")
            return

        course_code = self.tree.item(selected, "values")[0]
        self.tree.delete(selected)
        self.remove_course_from_csv(course_code)
        messagebox.showinfo("Success", f"Course {course_code} deleted successfully!")

    def search_course(self):
        keyword = self.search_entry.get().lower()
        for item in self.tree.get_children():
            self.tree.selection_remove(item)

        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if any(keyword in str(value).lower() for value in values):
                self.tree.selection_add(item)

    def course_exists(self, course_code):
        with open(self.csv_filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0].lower() == course_code.lower():
                    return True
        return False

    def remove_course_from_csv(self, course_code):
        all_courses = []
        with open(self.csv_filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0].lower() != course_code.lower():
                    all_courses.append(row)

        with open(self.csv_filename, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(all_courses)

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)

def main():
    root = tk.Tk()
    app = CourseInformationSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
