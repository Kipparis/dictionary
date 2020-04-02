def get_env(name, default=None):
    import os
    return (os.environ[name] if os.environ[name] else default)
