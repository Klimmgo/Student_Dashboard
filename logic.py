import webbrowser
import time
from resources import Resource
from data_management import load_student_data, save_student_data, load_resources, save_resources
from student import Student
from semester import Semester
from module import Modul, Grade
from study_program import Study_program

class Logic:
    """
    The Logic class serves as the core operational backbone of the student dashboard application, handling data processing, storage, and retrieval tasks. 
    It interacts with data storage files to load and save student information, modules, grades, and resources. 
    The class provides methods to add, edit, and delete modules and resources, update student information, and calculate academic progress metrics 
    such as total credits and average grades. It acts as an intermediary between the GUI and the application's data storage, 
    ensuring the UI layer remains separated from the data management logic.
    """
    def __init__(self, file_path='student_data.json'):
        self.file_path = file_path
        self.student = None
        self.resources = []
        self.initialize_data()

    def get_student_info(self):
        """
        Retrieves the current student's information for display in the GUI.

        Returns:
            dict: A dictionary containing the student's name, matriculation number,
                study program name, and study goal. Returns None if no student data is loaded.
        """
        if not self.student:
            return None  # Return None if no student data is loaded
        # Return a dictionary with relevant student information for the GUI
        return {
            "name": self.student.name,
            "matriculation_number": self.student.matriculation_number,
            "study_program": self.student.study_program.name,
            "study_goal": self.student.study_goal
        }

    def update_student_info(self, name, matriculation_number, study_program, study_goal):
        """
        Updates the stored student's information based on input from the GUI.

        Args:
            name (str): The student's name.
            matriculation_number (str): The student's matriculation number.
            study_program (str): The name of the student's study program.
            study_goal (float): The student's study goal.

        Returns:
            bool: True if the student information was successfully updated, False otherwise.
        """
        if self.student:
            # Update student information
            self.student.name = name
            self.student.matriculation_number = matriculation_number
            self.student.study_program.name = study_program
            self.student.study_goal = study_goal
            save_student_data(self.student, self.file_path)  # Save the updated information to file
            return True
        else:
            return False  # Return False if there is no student data to update

    def initialize_data(self):
        """
        Loads student data from the JSON file or initializes default data if the file is not found.
        """
        try:
            self.student = load_student_data(self.file_path)
        except FileNotFoundError:
            # Create a default study program instance with minimal details
            default_study_program = Study_program(name="Undeclared Program", total_credits=0)
            # Initialize the Student with the default study program
            self.student = Student(name="New Student", matriculation_number="000000", study_program=default_study_program)
            # Save the newly created student data for persistence
            save_student_data(self.student, self.file_path)

    def find_module_by_id(self, module_id):
        """
        Find a module by its ID across all semesters.

        :param module_id: The ID of the module to find.
        :return: Tuple containing the found module and its semester number, or (None, None) if not found.
        """
        for semester in self.student.study_program.semesters:
            for module in semester.modules:
                if module.id == module_id:
                    return module, semester.number
        return None, None

    def add_module(self, semester_number, name, credits, exam_type, grade_str):
        """
        Adds a new module to the student's study program.

        Args:
            semester_number (int): The number of the semester to which the module will be added.
            name (str): The name of the module.
            credits (int): The number of credits the module is worth.
            exam_type (str): The type of exam for the module (e.g., written, oral).
            grade_str (str): The grade received for the module, as a string. 'a' indicates accepted, 
                            numeric values are expected for actual grades.

        Returns:
            (bool, str): A tuple where the first element is a boolean indicating success, 
                        and the second element is a message detailing the result or error.
        """
        # Check if the specified semester exists, if not, create a new semester
        semester = self.student.study_program.get_semester(semester_number)
        if semester is None:
            semester = Semester(semester_number)
            self.student.study_program.add_semester(semester)

        # Generate a unique module ID
        module_id = f"module_{name.replace(' ', '_')}_{int(time.time())}"
        grade = None  # Default the grade to None

        # Validate and set the grade based on the input string
        if grade_str:
            try:
                # Determine if grade is 'a' for accepted or convert to float for numeric grades
                grade_value = 'a' if grade_str.strip().lower() == 'a' else float(grade_str)
                if not (grade_value == 'a' or (isinstance(grade_value, float) and 1.0 <= grade_value <= 5.0)):
                    raise ValueError("Grade must be 'a' or a number between 1.0 and 5.0.")
                grade = Grade(grade=grade_value)
            except ValueError as e:
                return False, f"Not a valid grade or 'a' for accepted. Please try again."

        # Attempt to add the module to the semester and save the updated student data
        try:
            new_module = Modul(id=module_id, name=name, credits=credits, exam_type=exam_type, grade=grade)
            semester.add_module_to_semester(new_module)  # Using the correct method name
            save_student_data(self.student, self.file_path)
            return True, "Module added successfully."
        except Exception as e:
            return False, f"Failed to add the module. Error: {str(e)}"

    def edit_grade(self, module_id, new_grade_str):
        """
        Edits the grade of an existing module identified by its module ID.

        Args:
            module_id (str): The unique identifier of the module whose grade is to be edited.
            new_grade_str (str): The new grade for the module, as a string. 'a' indicates accepted, 
                                numeric values are expected for actual grades.

        Returns:
            (bool, str): A tuple where the first element is a boolean indicating success, 
                        and the second element is a message detailing the result or error. 
                        An empty string is returned as the message upon success.
        """
        # Find the module by its ID
        module, _ = self.find_module_by_id(module_id)
        if not module:
            return False, "Module not found."

        try:
            # Determine the appropriate grade value or set to None for an empty string
            if new_grade_str.strip() == "":
                module.grade = None
            elif new_grade_str.strip().lower() == "a":
                module.grade = Grade(grade="a")
            else:
                new_grade = float(new_grade_str)
                module.grade = Grade(new_grade)
            save_student_data(self.student, self.file_path)
            return True, ""  # Indicate successful update
        except ValueError:
            return False, "Not a valid grade or 'a' for accepted. Please try again."

    def delete_module(self, module_id):
        """
        Deletes a module identified by its module ID from the student's study program.

        Iterates over the semesters to find and remove the specified module. If the module
        is successfully found and removed, it checks if the semester now contains no modules
        and removes the semester if it's empty. The student data is saved after the deletion.

        Args:
            module_id (str): The unique identifier of the module to be deleted.

        Returns:
            bool: True if the module was successfully deleted, False if the module was not found.
        """
        for semester in self.student.study_program.semesters:
            # Attempt to find the module to delete in the current semester
            module_to_delete = next((modul for modul in semester.modules if modul.id == module_id), None)
            
            if module_to_delete:
                # If found, remove the module from the semester
                semester.modules = [modul for modul in semester.modules if modul.id != module_id]
                
                # If the semester has no modules left, remove it from the study program
                if not semester.modules:  
                    self.student.study_program.remove_semester(semester.number)
                    
                save_student_data(self.student, self.file_path)  # Save the updated student data
                return True  # Module deletion successful
        return False  # Module not found, thus not deleted

    def get_resources(self):
        """
        Loads and returns the list of resources from storage.

        Attempts to load resources from the data storage. If the file containing
        resources does not exist, initializes an empty list of resources.

        Returns:
            list: A list of dictionaries, each representing a resource with its 'name' and 'url'.
                Returns an empty list if the resources file is not found.
        """
        try:
            self.resources = load_resources()  # Attempt to load resources from storage
        except FileNotFoundError:
            self.resources = []  # Initialize an empty list if the file does not exist
        return self.resources  # Return the list of resources

    def add_resource(self, name, url):
        """
        Adds a new resource to the list of resources and saves it to the JSON file.
        Assumes that name and URL are valid non-empty strings.
        """
        new_resource = Resource(name, url)
        resources = load_resources()
        resources.append(new_resource.to_dict())  # Convert to dictionary and append
        save_resources(resources)  # Save the updated list of resources

    def delete_resource(self, index):
        """
        Deletes a resource at the specified index from the list of resources
        and saves the updated list to the JSON file.
        """
        resources = load_resources()
        try:
            resources.pop(index)  # Attempt to remove the resource at the given index
            save_resources(resources)  # Save the updated list of resources
            return True
        except IndexError:
            return False  # Return False if there was an error

    def open_resource(self, index):
        """
        Opens a resource URL in the default web browser.

        Given an index, retrieves the resource's URL from the list of resources
        and opens it using the system's default web browser. This function assumes
        that the index is within the bounds of the resources list.

        Args:
            index (int): The index of the resource in the resources list to be opened.

        Returns:
            bool: True if the resource URL was successfully opened, False if the index is out of range.
        """
        if 0 <= index < len(self.resources):  # Check if index is within the range of the resources list
            resource_url = self.resources[index]['url']  # Retrieve the URL of the resource
            webbrowser.open(resource_url)  # Open the URL in the default web browser
            return True  # URL opening successful
        return False  # Index out of range, URL not opened

    def calculate_progress(self):
        """
        Calculates the student's progress towards their study program completion as a percentage.

        Progress is determined by the ratio of completed credits to total required credits.
        If no credits are required, progress is reported as 0 to avoid division by zero.

        Returns:
            float: Progress percentage, with 0 indicating no progress or no credits required.
        """
        total_credits = self.get_total_credits()  # Total credits in the program
        completed_credits = self.get_completed_credits()  # Credits the student has completed
        # Calculate progress percentage, ensuring no division by zero
        self.progress = (completed_credits / total_credits) * 100 if total_credits > 0 else 0
        return self.progress

    def calculate_average_grade(self):
        """
        Computes the student's average grade from all modules with numeric or float grades.

        The function excludes modules without grades or with non-numeric grades from the calculation.
        If there are no numeric grades to calculate, the function returns None.

        Returns:
            float or None: The average of numeric grades across all modules, or None if not applicable.
        """
        if not self.student:
            return None  # Return None if there's no student data
        
        # Collect all numeric grades from modules
        grades = [modul.grade.grade for semester in self.student.study_program.semesters for modul in semester.modules if modul.grade is not None and isinstance(modul.grade.grade, (int, float))]
        if grades:
            # Calculate and return the average if there are any grades to average
            return sum(grades) / len(grades)
        else:
            return None
    
    def get_total_credits(self):
        """
        Retrieves the total credits required by the study program.

        Returns:
        - The total number of credits.
        """
        return self.student.study_program.get_total_credits()

    def get_completed_credits(self):
        """
        Calculates and retrieves the number of credits the student has completed.

        Returns:
        - The total number of completed credits.
        """
        completed_credits = sum(modul.credits for semester in self.student.study_program.semesters for modul in semester.modules if modul.grade is not None and modul.status() in ['passed', 'accepted'])
        return completed_credits