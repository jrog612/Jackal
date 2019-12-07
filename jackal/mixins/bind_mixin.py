class BindMixin:
    bound_fields = []
    bind_field_name = 'extra'

    def __init__(self, *args, **kwargs):
        bind_data = {}
        for bound_field in self.bound_fields:
            value = kwargs.pop(bound_field, None)
            if value is not None:
                bind_data[bound_field] = value
        kwargs[self.bind_field_name] = bind_data
        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        if key in ['bound_fields', 'bind_field_name']:
            super().__setattr__(key, value)
        if key not in self.bound_fields or key == self.bind_field_name:
            super().__setattr__(key, value)
        else:
            bind_hash = getattr(self, self.bind_field_name, dict())
            bind_hash[key] = value
            setattr(self, self.bind_field_name, bind_hash)

    def __getattribute__(self, item):
        if item in ['bound_fields', 'bind_field_name']:
            return super().__getattribute__(item)
        elif item not in self.bound_fields or item == self.bind_field_name:
            return super().__getattribute__(item)
        else:
            bind_hash = getattr(self, self.bind_field_name, dict())
            return bind_hash.get(item)
