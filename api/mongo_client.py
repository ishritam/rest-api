import sys
sys.path.append(".")

import pymongo
import config



class MongoDb:
    def __init__(self):
        self.client=self.get_connection()

    def get_connection(self):
        """Creates a connection to mongodb

        Returns:
            [pymongo client]: returns a cursor to mongo
        """
        client = pymongo.MongoClient(config.MONGODB_URI)
        return client

    def close_connection(self):
        """Closes the connection
        """
        self.client.close()

    
    def execute_insert_one(self,collection_name,post):
        """Insert one audio document into collection

        Args:
            collection_name (String): Name of the collection to make changes
            post (Dict): dictionary containning audio detail

        Returns:
            [Bool]: returns task status
        """
        try:
            self.client[config.DB_NAME][collection_name].insert_one(post)
            return True,None
        except Exception as e:
            print(e)
            return False,e
    
    def execute_delete(self,collection_name,post):
        """Deletes document from collection

        Args:
            collection_name (String): Name of the collection to make changes
            post (Dict): dictionary containning audio detail

        Returns:
            [Bool]: returns task status
        """
        try:
            resp=self.client[config.DB_NAME][collection_name].remove(post)
            if resp['n']>0:
                return True,None
            else:
                return False,"Audio name does not exists"
        except Exception as e:
            print(e)
            return False,e

    def execute_update(self,collection_name,id,post):
        """Updates the movie detail 

        Args:
            collection_name (String): Name of the collection to make changes
            post (Dict): dictionary containning audio detail
            id (int): id of the audio to make changes

        Returns:
            [Bool]: returns task status
        """
        try:
            resp=self.client[config.DB_NAME][collection_name].update({"id":id},{"$set":post})
            print(resp)
            if resp['n']>0:
                if resp['nModified']>0:
                    return True,None
                else:
                    return False,"Unable to modify movie (maybe the update parameters are same)"
            else:
                return False,"Audio name does not exists"
        except Exception as e:
            print(e)
            return False,e

    

    def execute_search(self,collection_name,post):
        """Search the db and returns the result

        Args:
            collection_name (String): Name of the collection to make changes
            post (Dict): dictionary containning audio detail

        Returns:
            [Bool]: returns task status
        """
        try:
            result=list(self.client[config.DB_NAME][collection_name].find(post))
            return result
        except Exception as e:
            print("Error in executing mongo search ",post,e)
            raise


    
