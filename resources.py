import webbrowser

class Resource:
    """
    Represents an web resource with a name and a URL.
    """
    def __init__(self, name, url):
        self.name = name  # The resource's name (e.g., "IU Learn Platform")
        self.url = url  # The resource's URL

    def to_dict(self):
        """
        Serializes the Resource object into a dictionary for storage or transmission.
        
        Returns:
        - A dictionary containing the resource's name and URL.
        """
        return {'name': self.name, 'url': self.url}

    @staticmethod
    def from_dict(data):
        """
        Deserializes a dictionary into a Resource object.
        
        Parameters:
        - data: A dictionary with keys 'name' and 'url' representing a resource.
        
        Returns:
        - An instance of Resource initialized with the provided data.
        """
        return Resource(data['name'], data['url'])
