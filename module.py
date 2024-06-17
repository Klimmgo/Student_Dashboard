class Grade:
    """
    Represents a grade for a module including the exam type and the grade itself.
    """
    def __init__(self, grade):
        self.grade = grade # The actual grade received

    def to_dict(self):
        """
        Serialize the Grade object to a dictionary for JSON storage.
        
        Returns:
        - A dictionary representation of the Grade object.
        """
        return {'grade': self.grade}

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a dictionary into a Grade object.
        
        Parameters:
        - data: A dictionary containing the grade data.
        
        Returns:
        - An instance of Grade initialized with the provided data.
        """
        return cls(grade=data['grade'])

class Modul:
    """
    Represents an academic module or course, including details like ID, name, credits, exam type, and grade.
    """
    def __init__(self, id, name, credits, exam_type, grade=None):
        self.id = id # Unique identifier for the module
        self.name = name # Name of the module
        self.credits = credits # Number of credits awarded for completing the module
        self.exam_type = exam_type # Type of exam for the module
        self.grade = grade if grade is None or isinstance(grade, Grade) else Grade.from_dict(grade)  # The grade object

    def to_dict(self):
        """
        Serialize the Module object to a dictionary.
        
        Returns:
        - A dictionary representation of the Module object.
        """
        return {
            'id': self.id,
            'name': self.name,
            'credits': self.credits,
            'exam_type': self.exam_type,
            'grade': self.grade.to_dict() if self.grade else None
        }

    def status(self):
        """
        Determines the status of the module based on its grade.
        
        Returns:
        - A string indicating the status ('none', 'accepted', or 'passed').
        """
        if self.grade is None:
            return 'none'
        if isinstance(self.grade.grade, str) and self.grade.grade.lower() == 'a':
            return 'accepted'
        if isinstance(self.grade.grade, (int, float)) and self.grade.grade <= 4.0:
            return 'passed'
        return 'none'

    @classmethod
    def from_dict(cls, data):
        """
        Deserialize a dictionary into a Module object.
        
        Parameters:
        - data: A dictionary containing the module data.
        
        Returns:
        - An instance of Module initialized with the provided data.
        """
        grade = None
        if 'grade' in data and isinstance(data['grade'], dict):
            grade = Grade.from_dict(data['grade'])
        return cls(
            id=data['id'],
            name=data['name'],
            credits=data['credits'],
            exam_type=data['exam_type'],
            grade=grade
        )