from module import Modul

class Semester:
    """
    Represents an academic semester, containing multiple modules.
    """
    def __init__(self, number):
        self.number = number  # The semester number (e.g., 1 for the first semester)
        self.modules = []  # A list to store the semester's modules

    def add_module_to_semester(self, modul):
        """
        Adds a module to the semester.
        
        Parameters:
        - modul: An instance of Modul to be added to the semester.
        
        Raises:
        - TypeError: If the passed object is not an instance of Modul.
        """
        if not isinstance(modul, Modul):
            raise TypeError("Can only add instances of Modul.")
        self.modules.append(modul)

    def to_dict(self):
        """
        Serializes the Semester object into a dictionary.
        
        Returns:
        - A dictionary containing the semester number and a list of modules.
        """
        return {
            'number': self.number,
            'modules': [modul.to_dict() for modul in self.modules]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Deserializes a dictionary into a Semester object.
        
        Parameters:
        - data: A dictionary containing the semester data.
        
        Returns:
        - An instance of Semester initialized with the provided data.
        """
        semester = cls(data['number'])
        semester.modules = [Modul.from_dict(modul_data) for modul_data in data.get('modules', [])]
        return semester
