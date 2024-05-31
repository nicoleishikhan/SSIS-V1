import tkinter as tk
from tkinter import messagebox
from student import StudentInformationSystemGUI
from course import CourseInformationSystemGUI

class ElegantStudentSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_interface()

    def setup_interface(self):
        self.title("Student Management System")
        self.configure(bg="#f0f4f8")
        self.geometry("700x450")
        self.resizable(False, False)

        self.create_header()
        self.create_buttons()

    def create_header(self):
        header = tk.Label(
            self,
            text="Simple Student Information System",
            font=("Helvetica", 24, "bold"),
            bg="#bbdefb",
            fg="#0d47a1",
            pady=10
        )
        header.pack(side=tk.TOP, fill=tk.X, pady=20)

        instruction_label = tk.Label(
            self,
            text="Select an option to proceed:",
            font=("Helvetica", 16),
            bg="#f0f4f8",
            fg="#1976d2"
        )
        instruction_label.pack(pady=10)

    def create_buttons(self):
        button_style = {
            'font': ("Helvetica", 14),
            'bg': "#90caf9",
            'fg': "#0d47a1",
            'relief': tk.FLAT,
            'width': 25,
            'height': 2,
            'bd': 0
        }

        button_frame = tk.Frame(self, bg="#f0f4f8")
        button_frame.pack(pady=20)

        student_button = tk.Button(
            button_frame,
            text="Student Registration",
            command=self.open_student_registration,
            **button_style
        )
        student_button.pack(pady=10)

        course_button = tk.Button(
            button_frame,
            text="Course Registration",
            command=self.open_course_registration,
            **button_style
        )
        course_button.pack(pady=10)

        exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.quit_application,
            **button_style
        )
        exit_button.pack(pady=10)

    def open_student_registration(self):
        try:
            self.withdraw()
            student_window = tk.Toplevel(self)
            student_window.title("Student Registration")
            student_window.configure(bg="#f0f4f8")
            student_window.geometry("600x700")
            student_window.resizable(False, False)
            student_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_main(student_window))
            StudentInformationSystemGUI(student_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Student Registration: {e}")
            self.deiconify()

    def open_course_registration(self):
        try:
            self.withdraw()
            course_window = tk.Toplevel(self)
            course_window.title("Course Registration")
            course_window.configure(bg="#f0f4f8")
            course_window.geometry("600x700")
            course_window.resizable(False, False)
            course_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_main(course_window))
            CourseInformationSystemGUI(course_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Course Registration: {e}")
            self.deiconify()

    def return_to_main(self, window):
        if messagebox.askokcancel("Return", "Would you like to return to the main menu?"):
            window.destroy()
            self.deiconify()

    def quit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.destroy()

def start_app():
    app = ElegantStudentSystem()
    app.mainloop()

if __name__ == "__main__":
    start_app()
