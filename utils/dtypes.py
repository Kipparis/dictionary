class StringBool:
    '''If passed str object on init, check it's containing `True` or `False`,
    if passed int object, check 0 or 1'''
    def __init__(self, obj):
        if not obj: obj = 0 
        elif isinstance(obj,str):     # check for true, false
            if "true" in obj.lower(): obj = 1
            if "y" in obj.lower():    obj = 1
            obj = 0 
        else: obj = obj > 0     # if not str, than comparison is available
