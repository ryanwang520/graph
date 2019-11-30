import importlib
import pkgutil


def convert_snake_case_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def preload_module(pkg):
    if isinstance(pkg, str):
        pkg = importlib.import_module(pkg)
    for _, modname, _ in pkgutil.iter_modules(pkg.__path__):
        importlib.import_module("." + modname, pkg.__name__)


class ApiException(Exception):
    def __init__(self, message):
        self.message = message
