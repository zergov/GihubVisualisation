import logging
import os
from tinydb import TinyDB, Query

logger = logging.getLogger(__name__)

class CacheService:

    def __init__(self):

        # if db file doesnt exist (its gitignored), 
        # create it
        file_path = 'cache/db.json'
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

        self.db = TinyDB('cache/db.json')

    def query(self, repo_name):
        try:
            res = self.db.search(Query()['repo'] == repo_name)
            if res is not None:
                return (res[0]['commits'], res[0]['since'])
        except Exception as e:
            logger.error(f"Caching service : {e}")
            return ([], None)