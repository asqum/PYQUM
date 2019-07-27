from functools import wraps
def simple_decorator(func_with_docstring):
    # @wraps(func_with_docstring)
    def simple_wrapper(*args, **kwargs):
        """I should not see this simple docstring"""

        # do wrapper things
        value = func_with_docstring(*args, **kwargs)
        # do wrapper things
        return value
    return simple_wrapper

@simple_decorator
def simple_decorated_function(simple_arg, simple_kwargs='special string'):
    """I should see this simple docstring"""
    # do stuff
    return 'computed value'

def decorator_factory(fail_value='some fallback value'):
    def wrapper_factory(func_with_docstring):
        @wraps(func_with_docstring)
        def variable_wrapper(*args, **kwargs):
            """I should not see this factory docstring"""

            # do wrapper things
            value = func_with_docstring(*args, **kwargs)
            # do wrapper things
            return value
        return variable_wrapper
    return wrapper_factory

@decorator_factory(fail_value='different fallback value')
def factory_decorated_function(specific_arg, specific_kwarg=True):
    """I should see this factory docstring"""
    # do stuff
    return 'computed value'

print(simple_decorated_function.__doc__)
print(factory_decorated_function.__doc__)
