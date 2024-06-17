import json
from student import Student

def load_student_data(file_path='student_data.json'):
    """
    Load student data from a specified JSON file.
    
    Parameters:
    - file_path: The path to the JSON file containing the student data.
    
    Returns:
    - An instance of Student initialized with the data from the file.
    """
    # Open the file and load the JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Convert the JSON data into a Student object and return it
    return Student.from_dict(data)

def save_student_data(student, file_path='student_data.json'):
    """
    Save a Student object's data to a specified JSON file.
    
    Parameters:
    - student: The Student object to be saved.
    - file_path: The path to the JSON file where the data will be saved.
    """
    # Open the file for writing and dump the serialized Student object into it
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(student.to_dict(), file, ensure_ascii=False, indent=4)

def load_resources(file_path='resources.json'):
    """
    Load resources from a specified JSON file.
    
    Parameters:
    - file_path: The path to the JSON file containing resources data.
    
    Returns:
    - A list of dictionaries representing the resources, or an empty list if the file is not found.
    """
    
    try:
        # Attempt to open the file and load the JSON data
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data['resources']
    except FileNotFoundError:
        # Return an empty list if the file does not exist
        return []

def save_resources(resources, file_path='resources.json'):
    """
    Save resources to a specified JSON file.
    
    Parameters:
    - resources: A list of dictionaries representing the resources to be saved.
    - file_path: The path to the JSON file where the resources will be saved.
    """
    # Open the file for writing and dump the resources list into it
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump({'resources': resources}, file, ensure_ascii=False, indent=4)
