from neo4j import GraphDatabase
# import logging
# import sys
#
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# logging.getLogger("neo4j").addHandler(handler)
# logging.getLogger("neo4j").setLevel(logging.DEBUG)

class Neo4jConnection:

    def __init__(self, uri, user, pwd, database):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__db = database
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(
                self.__uri,
                auth=(self.__user, self.__pwd),
                database=self.__db,
                connection_acquisition_timeout=20
            )
            self.__driver.verify_connectivity()
        except Exception as e:
            print("Failed to create the driver:", e)
            raise e

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def read(self, get_fun, *args, **kwargs):
        result = None
        with self.__driver.session() as session:
            result = session.execute_read(get_fun, *args, **kwargs)
        session.close()
        return result

    def write(self, put_fun, *args, **kwargs):
        with self.__driver.session() as session:
            result = session.execute_write(put_fun, *args, **kwargs)
        session.close()
        return result

    def get_driver(self):
        return self.__driver