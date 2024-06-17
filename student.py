from study_program import Study_program

class Student:
    """
    Represents a student with personal information, study progress, and associated study program.
    """
    def __init__(self, name, matriculation_number, study_program):
        self.name = name  # The student's full name
        self.matriculation_number = matriculation_number  # Unique identifier for the student
        self.study_program = study_program  # Associated study program object

    def to_dict(self):
        """
        Serializes the Student object into a dictionary.

        Returns:
        - A dictionary representation of the Student object.
        """
        return {
            'name': self.name,
            'matriculation_number': self.matriculation_number,
            'study_program': self.study_program.to_dict(),
            'study_goal': self.study_goal
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserializes a dictionary into a Student object.

        Parameters:
        - data: A dictionary containing the student data.

        Returns:
        - An instance of Student initialized with the provided data.
        """
        study_program_instance = Study_program.from_dict(data['study_program'])
        student = cls(name=data['name'], matriculation_number=data['matriculation_number'], study_program=study_program_instance)
        student.study_goal = data.get('study_goal', 0.0)  # Optional study goal
        return student
