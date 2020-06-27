from peewee import *    # database handling
from datetime import datetime

# db = SqliteDatabase(None)

# # about fields
# # http://docs.peewee-orm.com/en/latest/peewee/models.html#fields
# class BaseModel(Model):
#     class Meta:
#         database = db   # this model uses the args.db_file database
#         # change table name, default to name of class
#         # table_name = string


# do not inherit base model so we can bind those models at run time
class Category(Model):
    '''
    list of existing caterogies
    '''
    name = CharField(default="")

# do not inherit base model so we can bind those models at run time
class Result(Model):
    '''
    table storing per-word score
    '''
    word        = CharField(default="") # foreign word
    native      = CharField(default="") # native translation
    description = CharField(default="")
    example     = CharField(default="") # sentence/word combination
    score = IntegerField(default=0)
    # default - current date
    last_modified_date = DateField(default=datetime.now)
    category           = ForeignKeyField(Category, backref="results")
