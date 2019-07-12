import json
import os
import sys
import csv
import urllib.parse
from collections import defaultdict
from crowdsourcing import db_, LS

dir_path = os.path.dirname(os.path.realpath(__file__))
task = 'label_sentence'
end_point_url = "" # need to get a new cluster
APP_URL = "XX.XX:XXX/" # need to get a new cluster
API_KEY = ""

JOB_ID = 'XXX' # task ls
JOB_TITLE = "XXX"
contributor_id = 'XXX'  # for test


TEMPLATE_DIR = os.path.join(dir_path, 'templates')
INSTRUCTION_HTML = os.path.join(TEMPLATE_DIR, 'f8_instruction_{}.html'.format(task))
INSTRUCTION_CML = os.path.join(TEMPLATE_DIR, 'f8_instruction_{}.cml'.format(task))
SEP = ';;'


def gen_confirmation_code(task_id):
    confirmation_code = str(int(task_id[::-1]) + 12345)
    return confirmation_code


def get_taskurl(taskids, task, is_debug=False): # for task 1 and 2. No role.
    base_url = 'localhost:8081/login?'
    str_tasks = SEP.join(taskids)
    if is_debug:
        params = {'task_ids': str_tasks, 'task': task, 'debug': 1}
    else:
        params = {'task_ids': str_tasks, 'task': task}
    url_str = base_url + urllib.parse.urlencode(params)
    return url_str


def calculate_reward(n, role, bonus=0):
    crowd_meta = {'base_reward_user': 0, 'base_reward_agent': 0}
    if n == 0:
        return 0
    key = 'base_reward_' + role
    if role == 'user':
        return crowd_meta[key] + bonus
    elif role == 'agent':
        a = n - 1
        return crowd_meta[key] * n + 0.1 * (a + a**2)//2 + bonus
    return 0


def generate_f8_task_json():
    pass


def gen_task_url_ls(csv_out, coll_in, task=LS, total_sent=20):
    task_ids = []
    total = 0
    csv_writer = csv.writer(open(csv_out, 'w'))
    csv_writer.writerow(["task", "total", "payment", "confirmation_code", "task_url"])
    lst_task_id = []
    d_group = defaultdict(list)
    for doc in coll_in.find({'is_subdoc_selected': True}):
        d_group[doc['doc_id']].append(doc['task_id'])
        if doc['doc_stats']['title'] > 1:
            lst_task_id.append(doc['task_id'])
    total_doc = 0
    for k, v in d_group.items():
        if len(v) in [2, 3] and total_doc < 10:
            total_doc += 1
            lst_task_id.extend(v)
    set_task_id = set(lst_task_id)
    total_labels = 0
    for doc in coll_in.find({'is_subdoc_selected': True}):
        if doc['task_id'] in set_task_id:
            task_ids.append(doc['task_id'])
            total += len(doc['label_ids'])
            total_labels += len(doc['label_ids'])
            if total > total_sent:
                job_url = get_taskurl(task_ids, task)
                confirmation_code = task_ids[-1][::-1]
                reward = "${}".format(float("{0:.2f}".format(0.1 * total)))
                reward = '$1.0'
                csv_writer.writerow([task, total, reward, confirmation_code, job_url])
                task_ids = []
                total = 0
    if task_ids:
        job_url = get_taskurl(task_ids, task)
        confirmation_code = task_ids[-1][::-1]
        reward = "${}".format(float("{0:.2f}".format(0.1 * total)))
        reward = '$1.0'
        csv_writer.writerow([task, total, reward, confirmation_code, job_url])
    print(total_labels)
                

if __name__ == '__main__':
    csv_out = os.path.join(dir_path, 'test.csv')
    gen_task_url_ls(csv_out, db_.task_TextAnno)