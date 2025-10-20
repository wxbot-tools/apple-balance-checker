class BaseModel:

    def __getattr__(self, item):
        if not hasattr(self, item):
            raise AttributeError
        return getattr(self, item)

    @classmethod
    def attr_setter(cls, obj, **kwargs):
        for key in kwargs:
            if key == 'self' or key == '__class__':
                continue
            setattr(obj, key, kwargs[key])

    @classmethod
    def empty_instance(cls):
        raise Exception('need implement by sub-class')

