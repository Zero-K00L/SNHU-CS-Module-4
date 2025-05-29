# author: John Grudzinski
# aac_crud.py

from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ Crud operations for Animal collection in MongoDB"""
    
    def __init__(self):
        """
        Initialize the MongoClient connection to the AAC database
        and set up the animals collection.
        """
        # Connection variable that are hard wired for the Apporto environment
        USER = "aacuser"
        PASS = "Mongomadness3241"
        HOST = "nv-desktop-services.apporto.com"
        PORT = 33090
        DB   = "AAC"
        COL  = "animals"
        
        # Create the MongoClient using the connection variables
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        # Select the database
        self.database = self.client['%s' % (DB)]
        # Select the collection
        self.collection = self.database['%s' % (COL)]
        
    def create(self, data):
        """
        Inserts a single document into the animals collection.
        
        Parameters
        ----------
        data : dict
            A dictionary representing the document to insert.

        Returns
        -------
        bool
            True if the insert operation was acknowledged; otherwise False.
            
        Raises
        -------
        Exception
            If the data parameter is None or empty.
        """
        # Validate that data is provided and is a dict.
        if data is not None:
            try:
                # Perform the insert operation
                self.collection.insert_one(data)
                return True
            except Exception as e:
                # Log the error and return False on failure
                print(f"[CREATE ERROR] {e}")
                return False
        else:
            # Raise an exception if no data to insert
            raise Exception("Nothing to save, because data parameter is empty")
            
            
    def read(self, query):
        """
        Queries the animals collection for documents matching the filter.
            
        Parameters
        ----------
        query : dict
            A dictionary specifying the find filter; if None, all docs are returned.

        Returns
        -------
        list of dict
            A list of matching documents. Returns an empty list on error.
        """
        # Default to an empty filter if none provided
        if query is None:
            query = {}
        try:
            # Perform the find operation and convert cursor to list
            cursor = self.collection.find(query)
            return list(cursor)
        except Exception as e:
            # Log the error and return an empty list on failure
            print(f"[READ ERROR] {e}")
            return []
        
    def read_by_id(self, id_str):
        """
        Find a single document by its _id string.
        
        Parameters
        ----------
        id_str : str
            The string representation of the MongoDB ObjectId (_id field).

        Returns
        -------
        dict or None
            The matching document as a dictionary, or None if not found
            or if an error occurs (e.g., invalid ObjectId string).
        """
        # Attempt to convert the input string to a valid ObjectId
        try:
            oid = ObjectId(id_str)
            # Query the collection by the _id field
            return self.collection.find_one({"_id": oid})
        except Exception as e:
            # Log the error (invalid id format, connection issues, etc.)
            print(f"[READ_BY_ID ERROR] {e}")
            return None





           