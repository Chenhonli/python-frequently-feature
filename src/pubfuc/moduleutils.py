"""Helper functions to handle object search in module"""
import inspect
from importlib import import_module
from pkgutil import iter_modules


def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For demo: walk_modules('scrapy.utils')
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def iter_classes(base_class, *modules, class_filter=None):
    """
    iterate the class within specified module paths satisfying the class filter
    :param base_class: the base class of the one to search
    :param modules: the module paths
    :param class_filter: the class filter
    :return:
    """
    for root_module in modules:
        for module in walk_modules(root_module):
            for obj in vars(module).values():
                if inspect.isclass(obj) and issubclass(obj, base_class) and obj.__module__ == module.__name__:
                    if not class_filter or class_filter(obj):
                        yield obj


def get_class(name, base_class, *modules):
    """
    get the first class with name as specified (with name-property or module name) in module paths
    :param name: the name to search for the class
    :param base_class: the base class of the one to search
    :param modules: the module paths
    :return:
    """
    for cls in iter_classes(base_class, *modules, class_filter=lambda x: x.__module__.split('.')[-1] == name):
        return cls
    return None
