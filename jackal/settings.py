from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed

DEFAULT_QUERY_FUNCTION = 'jackal.structures.DefaultQueryFunction'

DEFAULTS = {
    'STATUS_CONDITION_CLASSES': [],
    'STATUS_READABLE_CLASSES': [],
    'QUERY_FUNCTION_CLASSES': [
        DEFAULT_QUERY_FUNCTION
    ],
    'CUSTOM_STRUCTURES': {},

    'EXCEPTION_HANDLER': 'jackal.exceptions.jackal_exception_handler',
    'PAGE_LENGTH': 10,
    'APP_DIR': None,
    'UNKNOWN_READABLE': 'unknown',
    'DEFAULT_NONE_VALUES': ([], {}, '', None),
}

IMPORT_STRINGS = [
    'STATUS_CONDITION_CLASSES',
    'STATUS_READABLE_CLASSES',
    'QUERY_FUNCTION_CLASSES',
    'EXCEPTION_HANDLER',
    'CUSTOM_STRUCTURES',
]


class JackalSettings:
    def __init__(self, custom_settings=None, defaults=None, import_strings=None):
        if custom_settings:
            self._custom_settings = custom_settings

        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Jackal setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.custom_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    @property
    def custom_settings(self):
        if not hasattr(self, '_custom_settings'):
            self._custom_settings = getattr(settings, 'JACKAL', {})
        return self._custom_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_custom_settings'):
            delattr(self, '_custom_settings')


def perform_import(val, setting_name):
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    elif isinstance(val, dict):
        return {key: perform_import(item, setting_name) for key, item in val.items()}

    return val


def import_from_string(val, setting_name):
    try:
        module_path, class_name = val.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '%s' for Jackal setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


jackal_settings = JackalSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_jackal_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'JACKAL':
        jackal_settings.reload()


setting_changed.connect(reload_jackal_settings)
