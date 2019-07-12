from pymongo import MongoClient
from pathlib import Path
import json

DATA_FD = Path.home() / 'work' / 'data'
uri_local = 'mongodb://localhost'
cli = MongoClient(uri_local)
db_ = cli.demodb
LABEL_COLOR = {'p': 'orange-text', 's': 'blue-text', 'b': 'green-text', 'o': 'blue-grey-text'}
LABEL = {'p': 'precondition', 's': 'solution', 'b': 'both', 'o': 'other'}
LABEL_P = 'precondition'
LABEL_S = 'solution'
LABEL_B = 'both'
LABEL_O = 'other'

TITLE_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5']
SPLITTING_TAGS = ['h1', 'h2', 'h3']
LS = 'label_sentence'
LR = 'label_relation'
DOC = 'doc'
WRITE = 'write'

CLOUD_URL = "http://173.193.75.126:30113" # needs update