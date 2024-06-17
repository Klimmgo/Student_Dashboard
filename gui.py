import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GUI:
    """
    The GUI class is the graphical interface of the student dashboard application, responsible for creating and managing all visual elements of the application. 
    It encapsulates the layout, widgets, and event handling necessary for user interaction. 
    This class interacts with the Logic class to perform operations based on user input and to display data retrieved from the application's logic layer. 
    The class organizes the application's UI into frames for student information, module management, and resources, offering functionalities 
    such as adding, editing, and deleting modules and resources, updating student information, and visualizing academic progress.
    """
    def __init__(self, root, logic):
        """
        Initializes the Student Dashboard GUI.

        Parameters:
        - root: The root Tkinter window.
        - logic: from the logic class
        """
        self.root = root
        self.logic = logic
        self.module_tree_id_to_module_id = {} 
        self.root.title("Student Dashboard")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.resizable(False, False)
        
        self.load_icons()  # Load UI icons
        self.setup_ui()    # Setup UI components

    def load_icons(self):
        """Loads and scales icons for the application."""
        edit_image = Image.open("icons/edit_icon.png")
        save_image = Image.open("icons/save_icon.png")
        plus_image = Image.open("icons/plus_icon.png")
        minus_image = Image.open("icons/minus_icon.png")
        
        self.edit_icon = ImageTk.PhotoImage(edit_image.resize((16, 16), Image.Resampling.LANCZOS))
        self.save_icon = ImageTk.PhotoImage(save_image.resize((16, 16), Image.Resampling.LANCZOS))
        self.plus_icon = ImageTk.PhotoImage(plus_image.resize((16, 16), Image.Resampling.LANCZOS))
        self.minus_icon = ImageTk.PhotoImage(minus_image.resize((16, 16), Image.Resampling.LANCZOS))

    def setup_ui(self):
        """Sets up UI components."""
        self.create_student_info_frame()
        self.create_progress_frame()
        self.create_modules_frame()
        self.create_resources_frame()
        self.refresh_progress_frame()

    def toggle_edit(self):
        """
        Toggles the editability of the student information entries, allowing the user to update their information.
        Switches the icon of the edit button to indicate the current mode (edit or save).
        """
        if self.edit_button.cget('image') == str(self.edit_icon):
            # Enable text entry fields for editing
            self.name_entry.config(state=tk.NORMAL)
            self.matriculation_number_entry.config(state=tk.NORMAL)
            self.study_program_entry.config(state=tk.NORMAL)
            self.study_goal_entry.config(state=tk.NORMAL)
            self.edit_button.config(image=self.save_icon)
        else:
            # Disable text entry fields to prevent editing
            self.name_entry.config(state=tk.DISABLED)
            self.matriculation_number_entry.config(state=tk.DISABLED)
            self.study_program_entry.config(state=tk.DISABLED)
            self.study_goal_entry.config(state=tk.DISABLED)
            self.edit_button.config(image=self.edit_icon)

            # Collect edited values from entry fields
            name = self.name_var.get()
            matriculation_number = self.matriculation_number_var.get()
            study_program = self.study_program_var.get()
            study_goal = float(self.study_goal_var.get())  # Ensuring study_goal is a float

            # Call logic function to update and save the student data
            self.logic.update_student_info(name, matriculation_number, study_program, study_goal)

            # Refresh the UI with the updated data
            self.refresh_progress_frame()

    def create_student_info_frame(self):
        """
        Initializes and arranges the student information section in the GUI.
        This section displays the student's name, matriculation number, study program, and study goal.
        It also includes an edit button to allow the user to make changes to the student information.
        """
        # Initialize the frame
        frame = tk.LabelFrame(self.root, text="Student Information", padx=5, pady=13)
        
        # Position the frame in the first row, spanning three columns, aligned to the top left
        frame.grid(row=0, column=0, columnspan=3, sticky="nw", padx=10, pady=5)
        frame.config(width=265)  # Sets a fixed width for the frame

        # Get student info from the logic layer
        student_info = self.logic.get_student_info()  # Get student info from the logic layer
        
        # Initialize String Variables with values from student_info or empty string if None
        self.name_var = tk.StringVar(value=student_info.get("name", ""))
        self.matriculation_number_var = tk.StringVar(value=student_info.get("matriculation_number", ""))
        self.study_program_var = tk.StringVar(value=student_info.get("study_program", ""))
        self.study_goal_var = tk.StringVar(value=str(student_info.get("study_goal", "")))  # Converting study_goal to string

        # Create and place the 'Name' label and entry
        tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(frame, textvariable=self.name_var, state='readonly')
        self.name_entry.grid(row=0, column=1, sticky="w")

        # Create and place the 'Matriculation Number' label and entry
        tk.Label(frame, text="Matriculation Number:").grid(row=1, column=0, sticky="w")
        self.matriculation_number_entry = tk.Entry(frame, textvariable=self.matriculation_number_var, state='readonly')
        self.matriculation_number_entry.grid(row=1, column=1, sticky="w")

        # Create and place the 'Study Program' label and entry
        tk.Label(frame, text="Study Program:").grid(row=2, column=0, sticky="w")
        self.study_program_entry = tk.Entry(frame, textvariable=self.study_program_var, state='readonly')
        self.study_program_entry.grid(row=2, column=1, sticky="w")

        # Create and place the 'Study Goal' label and entry
        tk.Label(frame, text="Study Goal:").grid(row=3, column=0, sticky="w")
        self.study_goal_entry = tk.Entry(frame, textvariable=self.study_goal_var, state='readonly')
        self.study_goal_entry.grid(row=3, column=1, sticky="w")

        # Add the Edit button to enable editing of the student information
        self.edit_button = tk.Button(frame, image=self.edit_icon, command=self.toggle_edit)
        self.edit_button.grid(row=3, column=2, padx=10, sticky="w")

       # Configure the frame's layout for better appearance
        frame.grid_columnconfigure(0, weight=0)  # Label column doesn't expand
        frame.grid_columnconfigure(1, weight=1)  # Entry fields expand to fill the frame width
        frame.grid_columnconfigure(2, weight=0)  # Edit button column doesn't expand
        frame.grid_rowconfigure(3, weight=0)     # Rows don't expand vertically

    def create_progress_frame(self):
        """
        Initializes and arranges the progress overview section in the GUI.
        This section displays the student's academic progress, including total and completed credits,
        progress percentage, study goal achievement, and average grade. It also features a pie chart
        visualization of the progress.
        """
        self.progress_frame = tk.LabelFrame(self.root, text="Progress Overview")
        self.progress_frame.grid(row=0, column=1, sticky="nw", padx=10, pady=5)
        self.progress_frame.config(width=265, height=130)  # Sets fixed size for the frame
        self.progress_frame.grid_propagate(False)  # Prevent the frame from resizing based on content

        # Configures column widths for a consistent layout
        self.progress_frame.grid_columnconfigure(0, minsize=50)
        self.progress_frame.grid_columnconfigure(1, minsize=50)  # Reserved for the pie chart

        self.refresh_progress_frame() # Calls to initially populate the frame with data

    def create_resources_frame(self):
        """
        Creates and arranges the resources frame in the GUI.
        
        This frame includes a listbox displaying resources (like links to important websites),
        along with buttons to add and delete resources. The resources are loaded into the listbox
        through a separate function call to 'populate_resources_listbox'.
        """
        # Initialize the frame for resources within the main window
        self.resources_frame = tk.LabelFrame(self.root, text="Resources")
        self.resources_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
        self.populate_resources_listbox()

        # Initialize and place the Add Resource button
        self.add_button = tk.Button(self.resources_frame, image=self.plus_icon, command=self.add_resource_dialog)
        self.add_button.grid(row=0, column=2, padx=1, pady=1, sticky="nsew")

        # Initialize and place the Delete Resource button
        self.delete_button = tk.Button(self.resources_frame, image=self.minus_icon, command=self.delete_resource_dialog)
        self.delete_button.grid(row=1, column=2, padx=1, pady=1, sticky="nsew")

        # Ensure the resources listbox spans the necessary grid area
        self.resources_listbox.grid(row=0, column=0, rowspan=2, sticky="nsew")

    def create_modules_frame(self):
        """
        Creates and arranges the modules frame in the GUI.
        
        This frame includes a Treeview widget to display the student's modules, including details like
        module name, semester, credits, exam type, and grade. Also includes buttons for adding, editing,
        and deleting modules. Modules are loaded into the Treeview through 'populate_modules_tree'.
        """
        # Initialize the frame for modules within the main window
        frame = tk.LabelFrame(self.root, text="Modules")
        frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

        # Define the columns for the Treeview widget and configure their properties
        columns = ("Module", "Semester", "Credits", "Exam Type", "Grade")
        self.modules_tree = ttk.Treeview(frame, columns=columns, show="headings", height=25)
        self.modules_tree.grid(row=0, column=0, rowspan=3, sticky="nsew")

        # Configure each column's heading and width
        column_widths = {'Module': 450, 'Semester': 70, 'Credits': 70, 'Exam Type': 70, 'Grade': 70}
        for col in columns:
            self.modules_tree.heading(col, text=col.title())
            self.modules_tree.column(col, width=column_widths[col], anchor='center')

        # Initialize and place buttons for module management
        ttk.Button(frame, image=self.plus_icon, command=self.add_module_dialog).grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, image=self.edit_icon, command=self.edit_selected_module_grade).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, image=self.minus_icon, command=self.delete_selected_module).grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.populate_modules_tree()  # Load and display the list of modules

        # Adjust the treeview to span the columns of the buttons
        self.modules_tree.grid(row=0, column=0, sticky="nsew")

        # Configure the layout to allocate space appropriately
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

    def refresh_progress_frame(self):
        """
        Updates the progress frame with current academic progress and average grade.
        Displays the student's credits, progress percentage, study goal, and average grade.
        Also updates the pie chart visualization of the progress.
        """
         # Clear existing content
        for widget in self.progress_frame.winfo_children():
            widget.destroy()

        # Calculate the total and current credits
        total_credits = self.logic.get_total_credits()
        current_credits = self.logic.get_completed_credits()

        # Use the logic instance to calculate progress and average grade
        progress = self.logic.calculate_progress()
        average_grade = self.logic.calculate_average_grade()

        # Display credits
        tk.Label(self.progress_frame, text=f"Credits: {current_credits}/{total_credits}").grid(row=0, column=0, sticky="w")

        # Display the progress
        tk.Label(self.progress_frame, text=f"Progress: {progress:.2f}%").grid(row=1, column=0, sticky="w", pady=2)
        
        # Display the study goal with renamed label
        tk.Label(self.progress_frame, text=f"Study Goal: {self.study_goal_var.get()}").grid(row=2, column=0, sticky="w", pady=2)
        
        # Correctly handling the display and background color for average_grade
        goal = float(self.study_goal_var.get())  # Assumed this value is already validated
        if average_grade != "N/A":
            try:
                avg_grade_value = float(average_grade)
                avg_grade_text = f"Current Grade Average: {avg_grade_value:.2f}"
                bg_color = 'green' if avg_grade_value <= goal else 'red'
            except ValueError:
                avg_grade_text = "Current Grade Average: Error"  # Handle unexpected error
                bg_color = 'red'
        else:
            avg_grade_text = "Current Grade Average: N/A"
            bg_color = 'white'  # or any neutral color if average_grade is "N/A"

        avg_grade_label = tk.Label(self.progress_frame, text=avg_grade_text, bg=bg_color, fg='white')
        avg_grade_label.grid(row=3, column=0, sticky="w", pady=2)

        # Add pie chart visualization for progress
        figure = plt.Figure(figsize=(1, 1), dpi=100)
        figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        ax = figure.add_subplot(111)
        ax.pie([progress, 100 - progress], startangle=90, colors=['#4CAF50', '#FFC107'])
        ax.axis('equal')
        canvas = FigureCanvasTkAgg(figure, master=self.progress_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=1, rowspan=4, sticky="nswe", padx=5)

        # Configure the row and column sizes for proper alignment
        self.progress_frame.grid_rowconfigure(0, weight=0, pad=0)
        self.progress_frame.grid_rowconfigure(1, weight=0, pad=0)
        self.progress_frame.grid_rowconfigure(2, weight=0, pad=0)
        self.progress_frame.grid_rowconfigure(3, weight=0, pad=0)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_columnconfigure(1, weight=2)

    def populate_resources_listbox(self):
        """
        Populates the listbox in the resources frame with resource names.
        This method fetches resource information through the logic layer and displays each resource's name
        in the listbox widget for easy access. Double-clicking a resource name will open its URL in the web browser.
        It also configures a scrollbar for the listbox.
        """
        # If an existing listbox widget is present, destroy it to refresh the contents
        if hasattr(self, 'resources_listbox'):
            self.resources_listbox.destroy()

        # Create a new listbox widget for displaying the names of resources
        self.resources_listbox = tk.Listbox(self.resources_frame, height=4)
        self.resources_listbox.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # Bind a double-click event to the listbox to open the selected resource
        self.resources_listbox.bind('<Double-1>', self.on_resource_double_click)

        # Use the logic class to load resource names
        resources = self.logic.get_resources()
        for resource in resources:
            self.resources_listbox.insert(tk.END, resource['name'])

        # Configure the grid layout to allocate space for the scrollbar
        self.resources_frame.grid_columnconfigure(0, weight=1)
        self.resources_frame.grid_rowconfigure(0, weight=1)  # Listbox row
        self.resources_frame.grid_rowconfigure(0, weight=1)  # Add button row
        self.resources_frame.grid_rowconfigure(1, weight=1)  # Delete button row

        # Adding scrollbar to the listbox
        scrollbar = tk.Scrollbar(self.resources_frame, orient="vertical")
        scrollbar.grid(row=0, column=1, rowspan=2, sticky='nsew')

        # Set the listbox's yscrollcommand to the scrollbar's set command
        self.resources_listbox.config(yscrollcommand=scrollbar.set)

        self.configure_resources_listbox_scrollbar()

    def configure_resources_listbox_scrollbar(self):
        """
        Configures scrollbar for the resources listbox.
        """
        scrollbar = tk.Scrollbar(self.resources_frame, orient="vertical")
        scrollbar.grid(row=0, column=1, rowspan=2, sticky='nsew')
        self.resources_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.resources_listbox.yview)

    def populate_modules_tree(self):
        """
        Populates the treeview widget in the modules frame with module information.
        It displays each module's name, semester number, credits, exam type, and grade.
        Modules are tagged with different colors based on their status (e.g., passed, failed, no grade).
        This method also maintains a mapping between treeview item IDs and module IDs for easy management.
        """
        # Clear existing entries in the treeview
        self.modules_tree.delete(*self.modules_tree.get_children())
        # Reset the mapping between treeview IDs and module IDs
        self.module_tree_id_to_module_id.clear()
        
        # Define tags for color-coding module entries based on their status
        self.modules_tree.tag_configure('passed', background='#A2D5AB')  # Green
        self.modules_tree.tag_configure('failed', background='#FFC0CB')  # Red
        self.modules_tree.tag_configure('no_grade', background='#D3D3D3')  # Light grey

        # Iterate through each semester and module to add module information to the treeview
        for semester in self.logic.student.study_program.semesters:
            for module in semester.modules:
                # Determine the module's grade or use "N/A" if no grade is available
                grade = module.grade.grade if module.grade else "N/A"
                # Determine the appropriate tag based on the module's status
                if module.status() == 'accepted' or (module.grade and isinstance(module.grade.grade, (int, float)) and module.grade.grade <= 4.0):
                    tag = 'passed'
                elif module.grade and isinstance(module.grade.grade, (int, float)) and module.grade.grade == 5.0:
                    tag = 'failed'
                else:
                    tag = 'no_grade'
                
                # Insert the values into the tree with the appropriate tag
                tree_id = self.modules_tree.insert("", "end", values=(module.name, semester.number, module.credits, module.exam_type, grade), tags=(tag,))
                # Update the mapping with the new Treeview ID and module ID
                self.module_tree_id_to_module_id[tree_id] = module.id
        # Refresh the module frame with new information
        self.refresh_progress_frame()

    def add_resource_dialog(self):
        """
        Prompts the user for the new resource's name and URL through dialog boxes,
        then calls the logic to add the resource, and updates the GUI.
        """
        # Prompt the user for the name of the new resource
        name = simpledialog.askstring("Add Resource", "Enter the resource name:", parent=self.root)
        if not name or not name.strip():
            messagebox.showwarning("Add Resource", "The resource name cannot be empty.")
            return
        
        # Prompt for the URL of the new resource
        url = simpledialog.askstring("Add Resource", "Enter the resource URL:", parent=self.root)
        if not url or not url.strip():
            messagebox.showwarning("Add Resource", "The resource URL cannot be empty.")
            return
        
        # Add the new resource through the logic layer
        self.logic.add_resource(name, url)

        # Update the resources listbox in the UI
        self.populate_resources_listbox()

    def delete_resource_dialog(self):
        """
        Triggers a dialog to confirm resource deletion. If confirmed, it calls the logic
        layer's delete_resource method to perform the deletion.
        """
        selection = self.resources_listbox.curselection()
        if not selection:
            messagebox.showwarning("Delete Resource", "No resource selected.")
            return

        index = selection[0]  # Get the index of the selected item
        # Ask the user to confirm the deletion of the selected resource
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this resource?")
        if confirm:
            # Call the logic layer to delete the resource
            success = self.logic.delete_resource(index)
            if success:
                # Update the resources listbox in the UI
                self.populate_resources_listbox()
            else:
                messagebox.showerror("Delete Resource", "Failed to delete the selected resource.")

    def on_resource_double_click(self, event):
        """
        Called when a resource in the listbox is double-clicked. Opens the resource URL.
        """
        selection = self.resources_listbox.curselection()
        if selection:
            index = selection[0]  # Get the index of the selected item
            success = self.logic.open_resource(index)
            if not success:
                messagebox.showerror("Open Resource", "Failed to open the selected resource.")

    def edit_selected_module_grade(self):
        """
        Allows editing the grade of a selected module in the Treeview widget.

        Opens a dialog box for the user to input a new grade for the selected module.
        Validates the input grade and updates the module's grade through the logic layer.
        If the grade is successfully updated, the Treeview is refreshed to show the change.
        """
        # Retrieve the selected item from the Treeview
        selected_item = self.modules_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a module to edit its grade.")
            return

        # Extract the module ID from the selected item
        selected_item_id = selected_item[0]
        module_id = self.module_tree_id_to_module_id.get(selected_item_id)

        while True:
            # Prompt the user for a new grade
            new_grade_str = simpledialog.askstring(
                "Edit Grade",
                "Enter new grade (leave blank for no grade, enter 'a' for accepted):",
                parent=self.root
            )

            # If the user cancels the dialog, exit the loop
            if new_grade_str is None:
                return

            # Attempt to update the grade in the logic layer
            success, message = self.logic.edit_grade(module_id, new_grade_str)
            if success:
                self.populate_modules_tree()  # Refresh the treeview
                break  # Exit the loop if update was successful
            else:
                messagebox.showerror("Invalid Input", message) # Show error if update failed

    def delete_selected_module(self):
        """
        Deletes the selected module from the student's record.

        Confirms the deletion with the user before proceeding.
        If confirmed, it calls the logic layer to delete the module.
        The Treeview is refreshed to reflect the module's deletion.
        """
        # Retrieve the selected item from the Treeview
        selected_item = self.modules_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a module to delete.")
            return

        # Extract the module ID from the selected item
        selected_item_id = selected_item[0]
        module_id = self.module_tree_id_to_module_id.get(selected_item_id)
        
        # Confirm deletion with the user
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this module?")
        if confirm:
            # Delegate the deletion logic to the logic class
            deleted = self.logic.delete_module(module_id)
            if deleted:
                self.populate_modules_tree()  # Refresh the Treeview to remove the deleted module
            else:
                messagebox.showerror("Error", "Module could not be found.")  # Show error if module could not be deleted

    def add_module_dialog(self):
        """
        Initiates a dialog sequence to gather information for adding a new module.

        The dialog sequence prompts the user for the semester number, module name,
        credits, exam type, and optionally, the grade. Validates each input step by step,
        and if validation passes, the module is added to the student's record. The function
        loops for grade input until a valid grade is entered or the operation is canceled.
        Upon successful addition, the modules Treeview is refreshed to include the new module.
        """
        while True:
            # Prompt for the semester number of the new module
            semester_number = simpledialog.askinteger("Add Module", "Enter semester number:", parent=self.root)
            if semester_number is None:  # Check for dialog cancellation
                return

            # Prompt for the module's name
            name = simpledialog.askstring("Add Module", "Enter module name:", parent=self.root)
            if not name:  # Validate module name is not empty
                messagebox.showerror("Error", "Module name cannot be empty.")
                continue  # Re-prompt for the name

            # Prompt for the number of credits associated with the module
            credits = simpledialog.askinteger("Add Module", "Enter credits:", parent=self.root)
            if credits is None:  # Check for dialog cancellation
                return

            # Prompt for the type of exam associated with the module
            exam_type = simpledialog.askstring("Add Module", "Enter exam type:", parent=self.root)
            if not exam_type:  # Validate exam type is not empty
                messagebox.showerror("Error", "Exam type cannot be empty.")
                continue  # Re-prompt for the exam type

            # Inner loop for grade input with validation
            while True:
                grade_str = simpledialog.askstring("Add Module", "Enter grade (leave blank if not available):", parent=self.root)
                # Attempt to add the module with provided details, handling validation for the grade internally
                success, message = self.logic.add_module(semester_number, name, credits, exam_type, grade_str)
                if success:
                    self.populate_modules_tree()  # Refresh the modules Treeview with the new addition
                    return  # Exit the function upon successful module addition
                else:
                    messagebox.showerror("Error", message)  # Display specific error if module addition fails
                    if "grade" in message.lower():  # If the error is specifically related to the grade, prompt again
                        continue  # Prompt for grade again
                    else:
                        return  # Exit the function if the error is not related to the grade

    def run(self):
        """
        Starts the main event loop of the tkinter application. This method makes the application window responsive
        and interactive, allowing the user to perform actions within the GUI. It should be called once, after all
        the UI components have been initialized and configured.
        """
        self.root.mainloop() # Enter the tkinter main event loop
