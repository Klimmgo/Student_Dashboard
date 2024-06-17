from semester import Semester

class Study_program:
    """
    Represents an academic study program, consisting of multiple semesters and modules.
    """
    def __init__(self, name, total_credits):
        self.name = name  # The name of the study program
        self.total_credits = total_credits  # The total number of credits required to complete the program
        self.semesters = []  # A list to store the semesters within the program

    def add_semester(self, semester):
        """
        Adds a semester to the study program in chronological order.

        Parameters:
        - semester: An instance of Semester to be added.

        Raises:
        - ValueError: If the semester already exists within the program.
        """
        if not isinstance(semester, Semester):
            raise ValueError("Only Semester instances can be added.")
        if any(existing_semester.number == semester.number for existing_semester in self.semesters):
            raise ValueError(f"Semester {semester.number} already exists.")

        # Find the correct insertion index for the new semester to maintain order
        insertion_index = None
        for i, existing_semester in enumerate(self.semesters):
            if existing_semester.number > semester.number:
                insertion_index = i
                break
        
        # If a suitable position was found, insert the semester at that index
        if insertion_index is not None:
            self.semesters.insert(insertion_index, semester)
        else:
            # If no such position was found, it means this is the latest semester, so append it
            self.semesters.append(semester)

    def remove_semester(self, semester_number):
        """
        Removes a semester from the study program by its number.

        Parameters:
        - semester_number: The number of the semester to remove.
        """
        # Filter out the semester with the given number
        self.semesters = [semester for semester in self.semesters if semester.number != semester_number]
        # Additionally, check and remove any semesters without modules
        self.semesters = [semester for semester in self.semesters if semester.modules]

    def get_semester(self, semester_number):
        """
        Retrieves a semester by its number.

        Parameters:
        - semester_number: The number of the semester to retrieve.

        Returns:
        - The Semester object with the specified number, or None if not found.
        """
        for semester in self.semesters:
            if semester.number == semester_number:
                return semester
        return None

    def get_total_credits(self):
        """
        Calculates the total number of credits across all semesters and modules within the study program.

        Returns:
        - The total number of credits for the entire study program.
        """
        return sum(module.credits for semester in self.semesters for module in semester.modules)

    def to_dict(self):
        """
        Serializes the StudyProgram object into a dictionary for storage or network transfer.

        Returns:
        - A dictionary representation of the StudyProgram object, including names, total credits, and serialized semesters.
        """
        return {
            'name': self.name,
            'total_credits': self.total_credits,
            'semesters': [semester.to_dict() for semester in self.semesters]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserializes a dictionary into a StudyProgram object, including initializing semesters from serialized data.

        Parameters:
        - data: A dictionary containing serialized data of a study program.

        Returns:
        - An instance of StudyProgram initialized with the data from the dictionary.
        """
        study_program = cls(data['name'], data.get('total_credits', 0))
        study_program.semesters = [Semester.from_dict(sem) for sem in data.get('semesters', [])]
        # Recalculate total credits in case it's not provided or needs updating based on loaded semester data
        study_program.total_credits = study_program.get_total_credits()
        return study_program