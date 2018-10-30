import pymongo
from secret.secrets import DBAddress


def get_table(database: str, table: str):
    return pymongo.MongoClient(DBAddress)[database][table]
