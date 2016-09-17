HTML_HANDLERS = {}



def handler(tag):
    """Return a decorator registering a function handling ``tag`` elements."""
    def decorator(function):
        """Decorator registering a function handling ``tag`` elements."""
        HTML_HANDLERS[tag] = function
        return function
    return decorator


def test():
    print('hello')


@handler('tag')
test



print(HTML_HANDLERS)
