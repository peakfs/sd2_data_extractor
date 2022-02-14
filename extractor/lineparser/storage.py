"""
Contains classes that are responsible for storing the parsed line data.
"""


class BaseStorage:
    """
    Basic wrapper over a dictionary. Provides a simple way to store
    parsed line data.

    Contains the following:

        data:      dict This dictionary stores the parsed data.
        last_item: Any  This stores the last processed elements'
                            name. Usually lines starting with `export`
    """
    data = {}
    last_item = None

    def __init__(self):
        self.data = {}
        self.last_item = None
