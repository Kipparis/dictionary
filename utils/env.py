def get_env(name, default=None):
    import os
    return (os.environ.get(name, default))
