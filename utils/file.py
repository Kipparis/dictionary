import os
from datetime import datetime

def diff_m_time(lhf, rhf):
    return os.path.getmtime(lhf) - os.path.getmtime(rhf)

def update_mod_time(db_file):
    import time, datetime
    mod_time = time.mktime(datetime.datetime.now().timetuple())
    os.utime(db_file, (mod_time, mod_time))
