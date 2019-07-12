from pymongo import MongoClient
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
import json

DATA_FD = Path.home() / 'work' / 'data'
uri_local = 'mongodb://localhost'
cli = cli_l
db_ = cli.demodb
LABEL_FULLNAME = {'p': 'precondition', 's': 'solution', 'b': 'both', 'o': 'other'}
LABEL_P = 'precondition'
LABEL_S = 'solution'
LABEL_B = 'both'
LABEL_O = 'other'
LABELS = [LABEL_P, LABEL_S, LABEL_B, LABEL_O]
LABEL_COLOR = {'p': 'orange-text', 's': 'blue-text', 'b': 'green-text', 'o': 'blue-grey-text'}
LABEL_COLOR.update({LABEL_P: 'orange-text', LABEL_S: 'blue-text', LABEL_B: 'green-text', LABEL_O: 'blue-grey-text'})


TITLE_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5']
SPLITTING_TAGS = ['h1', 'h2', 'h3']
# TASK_LS = 'label_sentence'
# TASK_LR = 'label_relation'
# TASK_DOC = 'doc'
# TASK_WRITE = 'write'

TASK_LS = 'TextAnno'
TASK_LR = 'RelAnno'
TASK_DOC = 'DocAnno'
TASK_WRITE = 'DialAnno'

USER = 'user'
AGENT = 'agent'

SUCCESSFUL = True
UNSUCCESSFUL = False

POL_P = 'p'
POL_N = 'n'
POL_E = '-'

CLOUD_URL = "http://173.193.75.126:30113" # needs update

TASK_ID = 'task_id'
TEXT_ID = 'text_id'