import imp
import sys


def import_from_dotted_path(dotted_names, path=None):
    """
    :param dotted_names: dotted path to module e.g. ``'controllers.maas.alg1'``. Note, this must \
        be accessible from within the class path.
    :param path: if specified, will try to import this module from this path.

    :return: if dotted_names is ``'a.b.c'``, this function will be the equivalent of \
        ``from a.b import c; return c``.
    """
    # If the full dotted path has already been imported, return it
    if dotted_names in sys.modules:
        return sys.modules[dotted_names]
    if '.' in dotted_names:
        next_module, remaining_names = dotted_names.split('.', 1)
    else:
        next_module, remaining_names = dotted_names, ''

    # If next_module has already been imported, don't reload it
    if next_module in sys.modules:
        module = sys.modules[next_module]
    else:
        fp, pathname, description = imp.find_module(next_module, path)
        try:
            module = imp.load_module(next_module, fp, pathname, description)
        finally:
            if fp:
                fp.close()

    # Class, constant, etc in a module; return it
    if hasattr(module, remaining_names):
        return getattr(module, remaining_names)

    # Last iteration, return the module
    if not remaining_names:
        return module
    return import_from_dotted_path(remaining_names, path=module.__path__)
