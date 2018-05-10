from injection.exceptions import InjectionKeyError


__all__ = ['inject', 'exceptions', 'InjectionKeyError']


def inject(module=None, attrib=None):
    '''
    inject: provides module injection via decorators.

    :param (string) module:
    :param (string) attrib:

    :raises InjectionKeyError:

    Examples:
        >>>@inject('time')
        >>>def test_module_import(module):
        >>>    if module is None:
        >>>        print("could not import check console for error :(")
        >>>    else:
        >>>        print("print module {} successfully imported".format(module))
        >>>@inject('time', 'sleep')
        >>>def sleep(function):
        >>>    if function is None:
        >>>        print("could not import function! check console for error :(")
        >>>    else:
        >>>        print("taking a quick nap...")
        >>>        function(1)  # sleep for 1 second
        >>>       print("what a nice nap :)")
        >>>@inject('time', 'altzone')
        >>>def print_module_variable(variable):
        >>>    if variable is None:
        >>>        print("could not import variable! check console for error :(")
        >>>    else:
        >>>        print("altzone: {}".format(variable))
        >>>@inject('time')
        >>>class InjectedClass:
        >>>    def __init__(self, module):
        >>>        self.module = module
        >>>        print("Injected Class at: {}".format(self.module.time()))
        >>>@inject('time')
        >>>@inject('urllib')
        >>>def multiple_injections(urllib, time):
        >>>    print(urllib)
        >>>    print(time)
    '''

    if module is None:
        raise InjectionKeyError("injection missing key: module!")

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            mod = None
            try:
                mod = __import__(module)
                if attrib is not None:
                    mod = getattr(mod, attrib)
            except ImportError as e:
                raise ImportError("[ inject ] could not inject module: {} with attribute: {} , as:\n{}".format(module, attrib, e))

            res = func(*args, mod, **kwargs)
            return res
        return inner_wrapper
    return wrapper
