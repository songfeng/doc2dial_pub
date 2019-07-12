import collections
import itertools
import random
import datetime
from collections import Counter, defaultdict
import copy
import operator
from bs4 import BeautifulSoup

from ..main.const import *  
from ..main.utils import randomword
from .. import config, db_


fmt = '%Y-%m-%d %H:%M:%S.%f'


def _update_html_label(html, d_label, task=TASK_DOC, is_hide_tag=False):
    soup = BeautifulSoup(html, "html.parser")
    for k, v in d_label.items():
        tag = soup.find(attrs={'text_id': k})
        if not tag:
            continue
        for ele in v:
            if not ele: continue
            attrs_div = {'class': 'chip ' + LABEL_COLOR.get(ele[0], '')}
            new_span = soup.new_tag('span', **attrs_div)
            new_span.string = ele + '[{}]'.format(k) 
            if task == TASK_LS:
                tag['class'] = LABEL_COLOR.get(ele[0], '')
                tag.insert(1, new_span)
            # elif task == TASK_LR:
            #     if len(tag.contents) > 2:
            #         tag.insert(len(tag.contents) + 1, new_span)
            #     else:
            #         tag.insert(len(tag.contents), new_span)
        if is_hide_tag:
            tag = soup.find(attrs={'label_id': k})
            tag['style'] = 'display: none'
    return str(soup)


def get_task_db(session):
    coll_name = config['domain_db']['coll_task_data'] + session[TASK]
    return db_[coll_name]


def get_crowd_info_db(session):
    coll_name = config['domain_db']['coll_crowd_info'] + session[TASK]
    if session[DEBUG]:
        coll_name += '_test'
    return db_[coll_name]


def get_crowd_data_db(session, is_debug=None):
    coll_name = config['domain_db']['coll_crowd_data'] + session[TASK]
    if not is_debug:
        is_debug = session[DEBUG]
    if is_debug:
        coll_name += '_test'
    return db_[coll_name]


def load_quiz_data(session):
    labels = ['q_{}'.format(ele) for ele in range(1, 7)]
    choices = [('P', 'Precondition(P)'), ('S', 'Solution(S)'), ('B', 'Both(B)'), ('O','Other(O)')]
    quiz_data = {'choices': choices, 'labels': labels, 'question': 'question text'}
    return quiz_data


def examine_user_input(d_in, session=None):
    sys_msg = 'Please complete all the labels. Thanks!'
    # for k, v in d_in.items():
    #     sys_msg = '<div class="grey-text">Please try again.</div>'
    #     return True, sys_msg
    return True, sys_msg


def get_ts_str():
    return str(datetime.datetime.now())


def get_role_other(role_other, task_id, is_debug):
    db_crowd = get_crowd_data_db(is_debug)
    ts_other, ts_curr = None, None
    username_other = None
    for r in db_crowd.find({TASK_ID: task_id}):
        if r[ROLE] == role_other:
            ts_other = datetime.datetime.strptime(str(r[TS]), fmt)
            username_other = r[USERNAME]
        else:
            ts_curr = datetime.datetime.strptime(str(r[TS]), fmt)
    if ts_other and ts_curr:
        delta = abs((ts_curr - ts_other).total_seconds())
        if delta < 60 * 10:
            return True, username_other
    return False, username_other


def get_task_count(role, worker_id, is_debug):
    db_crowd = get_crowd_data_db(is_debug)
    db_crowd.find({WORKER_ID: worker_id, ROLE: role}).count()


def insert_crowd_info(session, d_data={}):
    coll = get_crowd_info_db(session)
    d_data.update(session)
    d_data.update({TS: get_ts_str()})
    for k in [TEST, USERNAME, ROLE, FEEDBACK]:
        d_data[k] = session.get(k)
    for k in ['csrf_token', 'is_debug', 'task_ids', 'next_task_idx', '_id']:
        d_data.pop(k, None)
    coll.insert_one(d_data)


def insert_anno_data(session, d_data):
    coll = get_crowd_data_db(session)
    d_data.update(session)
    d_data.update({TS: get_ts_str()})
    # for k in [TASK_ID, USERNAME, WORKER_ID, ROLE, TURN, MODE]:
    for k in ['csrf_token', 'is_debug', 'task_ids', 'next_task_idx', '_id']:
        d_data.pop(k, None)
    coll.insert_one(d_data)


def get_dial_id(session):
    coll_task = get_task_db(session)
    dial_id = None
    for r in coll_task.find({TASK_ID: session[TASK_ID]}):
        dial_id = r[DIAL_ID]
    return dial_id


def get_chatdata(session):
    coll = get_crowd_data_db(session)
    dial_id = get_dial_id(session)
    history = [{MSG: 'How may I help you?', ROLE: AGENT}]
    for r in coll.find({DIAL_ID: dial_id}).sort("$natural", 1):
        if 'input_text' in r['labels']:
            msg = r['labels']['input_text'].strip()
            if msg:
                history.append({ROLE: r[ROLE], MSG: msg})
    return history[:session[TURN_ID]]


def load_task_ids(session):
    coll_task = get_task_db(session)
    lst_task_id = []
    for d_doc in coll_task.find({'doc_id': session[DOC_ID]}):
        # if d_doc.get('is_doc_selected', True) or d_doc.get('is_subdoc_selected', True):
        lst_task_id.append(d_doc[TASK_ID])
    return lst_task_id


def load_task_ids_write(session):
    coll_task = get_task_db(session)
    coll_crowd = get_crowd_data_db(session)
    lst_task_id = []
    for d_doc in coll_task.find({'doc_id':session[DOC_ID]}):
        # if d_doc.get('is_doc_selected', True) or d_doc.get('is_subdoc_selected', True):
        if 'anno_w' in d_doc: 
            continue
        turn_id = d_doc[TURN_ID]
        dial_id = d_doc[DIAL_ID]
        if turn_id > 1:
            task_id_t = None
            for d_doc_t in coll_task.find({DIAL_ID: dial_id, TURN_ID: turn_id - 1}):
                task_id_t = d_doc_t[TASK_ID]
            d_labels = None
            for d_doc_c in coll_crowd.find({TASK_ID: task_id_t}):
                if 'input_text' in d_doc_c['labels'] and ('evaluation' not in d_doc_c or not d_doc_c['evaluation']):
                    # select one hasn't been annotated
                    d_labels = d_doc_c['labels']
                    break
            if d_labels:
                lst_task_id.append(task_id_t)
                coll_task.update_one({'_id': d_doc_t['_id']}, {"$set": {"anno_w": d_labels}})
        lst_task_id.append(d_doc[TASK_ID])
    return lst_task_id
                

def get_next_doc(session):
    coll_crowd_task = get_task_db(session)
    for doc in coll_crowd_task.find({DOC_ID: session[DOC_ID]}):
        idx = doc['idx_doc'] + 1
        for doc_next in coll_crowd_task.find({'idx_doc': idx}):
            return doc_next
    return None


def load_label_tasks(session):
    task = session[TASK]
    task_id = session[TASK_ID]
    coll_task = get_task_db(session)
    coll_crowd_data = get_crowd_data_db(session, False)
    for d_task in coll_task.find({TASK_ID: task_id, TASK: task}):
        d_task.pop('_id', None)
        for data in coll_crowd_data.find({'task_id': session[TASK_ID]}):
            if task == TASK_LS and 'labels' in data and data['labels'] and session[DEBUG]:
                d_task['task_html'] = _update_html_label(d_task['task_html'], data['labels'], task)
                return d_task
        if 'anno_ls' in d_task and task in [TASK_LS, TASK_LR] and session[DEBUG]:
            d_task['task_html'] = _update_html_label(d_task['task_html'], d_task['anno_ls'], task)
            return d_task
        return d_task
    return None


def update_crowd(coll_crowd, r_id, session):
    r = {TS: get_ts_str()}
    for k in [WORKER_ID, TEST]:
        r[k] = session.get(k)
    coll_crowd.update({'_id': r_id}, {'$set': r})


def is_pass_test(session, worker_id):
    db_crowd = get_crowd_info_db(session)
    if worker_id in ['test123']:
        return True
    for r in db_crowd.find({WORKER_ID: worker_id}):
        if r[TEST]:
            return True
    return False


def get_user(username):
    coll = db_.get_collection('users')
    for d_doc in coll.find({"username": username}):
        return d_doc
    return {'username': 'admin', 'password': 'admin'}