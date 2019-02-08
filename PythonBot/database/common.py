import pymongo
from secret.secrets import DBAddress, DBName, DBPassword


def get_table(database: str, table: str):
    return pymongo.MongoClient(DBAddress, username=DBName, password=DBPassword)[database][table]
