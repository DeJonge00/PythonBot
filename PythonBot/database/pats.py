from database.common import get_table

PAT_DATABASE = 'pats'
PAT_TABLE = 'pats'


# Returns current pat amount
def increment_pats(patter_id: str, pattee_id: str):
    table = get_table(PAT_DATABASE, PAT_TABLE)
    table.update({'patter': patter_id, 'pattee': pattee_id}, {'$inc': {'pats': 1}}, upsert=True)
    return table.find({'patter': patter_id, 'pattee': pattee_id})[0].get('pats')
