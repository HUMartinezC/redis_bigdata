import redis
import json

class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    # -------------------------------
    # Operaciones CRUD Reutilizables
    # -------------------------------
    def set(self, key, value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.r.set(key, value)


    def get(self, key):
        value = self.r.get(key)
        try:
            return json.loads(value)
        except:
            return value

    def delete(self, key):
        val = self.get(key)
        self.r.delete(key)
        return val

    def keys(self, pattern="*"):
        return self.r.keys(pattern)

    def mget(self, keys):
        return [self.get(k) for k in keys]

    def exists(self, key):
        return self.r.exists(key)

    # ---------- Métodos de listas ----------
    def rpush(self, key, *values):
        return self.r.rpush(key, *values)

    def lrange(self, key, start=0, end=-1):
        return [v.decode("utf-8") if isinstance(v, bytes) else v for v in self.r.lrange(key, start, end)]

    def type(self, key):
        t = self.r.type(key)
        if isinstance(t, bytes):
            return t.decode("utf-8")
        return t

    # ---------- Métodos de sets ----------
    def sadd(self, key, *values):
        return self.r.sadd(key, *values)

    def smembers(self, key):
        return self.r.smembers(key)
    
    # ---------- Limpiar toda la DB ----------
    def flushdb(self):
        self.r.flushdb()
