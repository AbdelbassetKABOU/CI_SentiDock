from redis import Redis

r = Redis(host='redis', port=6379)
#r = Redis(host='172.17.0.2', port=6379)

def get_redis_dict(redis_dict: dict) -> dict :
    redis_database = {}
    redis_items = list(r.lrange(redis_dict,0,-1))
    redis_items = [x.decode('UTF-8') for x in redis_items]
    for item in redis_items :
        item_detail = r.hgetall(item)
        item_dict = {}
        for key, value in item_detail.items():
            item_dict[key.decode('utf-8')] = value.decode('utf-8')
        redis_database[item] = item_dict
    return redis_database

users_database = get_redis_dict('users')
sentences_database = get_redis_dict('sentences')



