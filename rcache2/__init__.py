import json
import hashlib


class RedisCRUD:
    def __init__(self, redis):
        self.redis = redis

    def read(self, key):
        value = self.redis.get(key)
        if value:
            return json.loads(value)

    def create(self, key, value):
        if value:
            self.redis.set(key, json.dumps(value))

    def delete(self, key):
        self.redis.delete(key)

    def update(self, key, value):
        self.create(key, value)


def key_hash_generator(func ,*args, **kwargs):
    return f"{func.__name__}:{hashlib.md5(f'{args}:{kwargs}'.encode('utf-8')).hexdigest()}"


class Rcache:
    @classmethod
    def init(
        cls,
        db,
        key_generator=key_hash_generator
    ):
        cls._db = RedisCRUD(db)
        cls.key_generator = key_generator

    @classmethod
    def get_session(cls):
        return cls._db   


class Cache:
    def __init__(self, func):
        self.func = func
        self.key_generate = Rcache.key_generator
        self.session = Rcache.get_session()

    def __call__(self, *args, **kwargs):
        hash_key_func = self.key_generate(self.func, *args, **kwargs)
        value = self.session.read(hash_key_func)
        if not value:
            value = self.func(*args, **kwargs)
            self.session.create(hash_key_func, value)
        return value

    def cache_delete(self, *args, **kwargs):
        hash_key_func = self.key_generate(self.func, *args, **kwargs)
        self.session.delete(hash_key_func)

    def cache_update(self, *args, **kwargs):
        self.hash_key_func = self.key_generate(self.func, *args, **kwargs)
        return self
    
    def value(self, value):
        self.session.update(self.hash_key_func, value)
