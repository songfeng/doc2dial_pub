from flask import session, redirect, url_for, request, jsonify
from flask import render_template, render_template_string
import json
from . import app
from .. import config
from ..main.data import get_next_doc, get_user
from ..main.forms import (AdminLoginForm, WorkerLoginForm, TestForm, ResultForm,
                    FeedbackForm, AnnotationDocForm, AnnotationWriteForm, AnnotationLabelForm, AnnotationLabelRelationForm)
from ..main.data import (insert_anno_data, is_pass_test, insert_crowd_info, examine_user_input,
                   get_dial_id, update_crowd, load_quiz_data, load_task_ids, load_task_ids_write, load_label_tasks)
from ..main.const import *
from ..main.metadata_processor import metadata_valuetype


def verify_admin(username, password):
    return True
    user = get_user(username)
    if user['password'] == password:
        print("Login for {} successful!!!".format(username))
        return True
    else:
        print("Login attempted for {}. Incorrect password used.".format(username))
    return False


def verify_worker(worker_id):
    # TODO Add logic to take worker_id and compare against trusted workers from Figure8
    return True


@app.route('/example', methods=['GET', 'POST'])
def example():
    return render_template('examples.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    d_in = form_POST(None)
    d_answer = {'quiz_answer':['P', 'S', 'B', 'P', 'S', 'P']}
    insert_crowd_info(session)
    print('$$', d_in)
    d_res = {}
    return jsonify(d_res)


@app.route('/test', methods=['GET', 'POST'])
def test():
    username = session.get(USERNAME)
    is_pass = session.get(PASS)
    task_id = session.get(TASK_ID)
    form = TestForm()
    # if request.method == 'POST':
    #     answer = ['O'] * 6
    #     data = [form.q1.data, form.q2.data, form.q3.data, form.q4.data, form.q5.data, form.q6.data,]
    #     is_pass = len([1 for i in range(len(answer)) if answer[i] == data[i]]) > 1
        
        # result_page = 'result.{}.html'.format(session[TASK])
        # form1 = ResultForm()
        # is_pass = True
        # return render_template(result_page, form=form1)
        # print(len([1 for i in range(len(answer)) if answer[i] == data[i]]))
        # if is_pass:
        #     session[PASS] = is_pass
        #     _id = None
            # for r in db_crowd.find({TASK_ID: task_id}):
            #     _id = r['_id']
            #     break
        #     if not _id:
        #         insert_crowd_info(session, {})
        #     else:
        #         update_crowd(_id, session, {})
        #     return redirect(url_for('.label'))
        # else:
        #     return redirect(url_for('.end'))
  
    html_page = 'quiz.{}.html'.format(session[TASK])
    quiz_data = load_quiz_data(session)
    text_data = ''
    return render_template(html_page, form=form, text_data=text_data, quiz_data=quiz_data, username=username)


def _init_login_by_form(form):
    session.clear()
    session[WORKER_ID] = form.workerid.data
    session[USERNAME] = form.username.data
    session[TASK_IDS] = form.task_ids.data
    session[TASK] = form.task.data
    session[DOC_ID] = form.doc_id.data
    session[NEXT_TASK_IDX] = 0
    if len(session[TASK_IDS].strip()) > 0:
        if SEP in session[TASK_IDS]:
            session[TASK_IDS] = session[TASK_IDS].split(SEP)
        else:
            session[TASK_IDS] = [session[TASK_IDS]]
    # elif session[TASK] == TASK_WRITE: 
    #     session[TASK_IDS] = load_task_ids_write(session)
    else:
        session[TASK_IDS] = load_task_ids(session)


def configure_session_for_admin(form):
    session.clear()
    session[USERNAME] = form.username.data
    session[TASK_IDS] = form.task_ids.data

    # Map task names to their corresponding task identifier
    task = form.task.data
    session[TASK] = task

    session[DOC_ID] = form.document.data
    session[NEXT_TASK_IDX] = 0
    session[DEBUG] = True

    # If multiple task_ids are provided then separate them and return a list
    if len(session[TASK_IDS].strip()) > 0:
        if SEP in session[TASK_IDS]:
            session[TASK_IDS] = session[TASK_IDS].split(SEP)
        else:
            session[TASK_IDS] = [session[TASK_IDS]]
    # If not task_id is provided task is 'write' then load task ids
    # elif session[TASK] == TASK_WRITE:
        # session[TASK_IDS] = load_task_ids_write(session)
    else:
        session[TASK_IDS] = load_task_ids(session)


def configure_session_for_worker(worker_id: str, username: str, task: str, task_ids: list = None):
    session.clear()
    session[WORKER_ID] = worker_id
    session[USERNAME] = username
    session[TASK] = task

    session[NEXT_TASK_IDX] = 0
    session[DEBUG] = True

    if task_ids:
        session[TASK_IDS] = task_ids
    # If not task_ids aren't provided then load task ids
    elif session[TASK] == TASK_WRITE:
        session[TASK_IDS] = load_task_ids_write(session)
    else:
        session[TASK_IDS] = load_task_ids(session)


def form_POST(form_meta):
    d_in = {}
    for k_, v_ in request.args.items():
        if '[' in k_:
            k = k_.split('[')[0]
            if k not in d_in:
                d_in[k] = [v_]
            else:
                d_in[k].append(v_)
        else:
            d_in[k_] = v_
    if form_meta is None:
        return d_in
    lst_single_value, lst_multiple_value = metadata_valuetype(form_meta)
    for label, data_type in lst_single_value:
        if data_type in [INTEGER, FLOAT, STRING]:
            MAP = {INTEGER: int, FLOAT: float, STRING: str}
            val = request.args.get(label, type=MAP[data_type])
            if val:
                d_in[label] = val
    for label, data_type in lst_multiple_value:
        if data_type in [STRING]:
            vals = request.args.getlist(label + "[]", type=str)
            d_in[label] = vals
        elif data_type in [INTEGER]:
            d_in[label] = request.args.getlist(label + "[]", type=int)
        elif data_type in [FLOAT]:
            d_in[label] = request.args.get(label, 0, type=float)
    return d_in


@app.route('/anno', methods=['GET', 'POST'])
def anno():
    session.pop(NEXT_TASK_IDX)
    if session[TASK] == TASK_WRITE:
        d_in = form_POST(config['metadata'][TASK_WRITE])
        session[DIAL_ID] = get_dial_id(session)
    else:
        d_in = form_POST(None)
    print('$$d_in', d_in)
    d_res = {}
    is_pass, sys_msg = examine_user_input(d_in, session)
    if is_pass:
        session[NEXT_TASK_IDX] = int(d_in[NEXT_TASK_IDX]) + 1
        d_in.pop(NEXT_TASK_IDX)
        if session[TASK] in [TASK_LS, TASK_LR] and len(d_in) > 0:
            if session[TASK] == TASK_LS:
                s = json.dumps(d_in)
                for k, v in LABEL_FULLNAME.items():
                    s = s.replace(k, v)
                d_in = json.loads(s)
            insert_anno_data(session, {'labels': d_in})
        elif session[TASK] == TASK_WRITE:
            if (d_in.get('input_text'), None) or d_in.get('approval', None):
                insert_anno_data(session, {'labels': d_in})
    d_res['is_pass'] = is_pass
    d_res['sys_msg'] = "Label saved." # sys_msg
    return jsonify(d_res)
    # return 'Okay'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AdminLoginForm()
    if DEBUG not in session:
        session[DEBUG] = True

    if form.validate_on_submit():
        if not verify_admin(form.username.data, form.password.data):
            form.password.errors = ["You have entered an invalid username or password."]

        else:
            configure_session_for_admin(form)
            session[DEBUG] = True
            session[PASS] = True

            return redirect(url_for('.label'))
    return render_template('index.{}.html'.format(config['domain_name']), form=form, is_debug=True)


@app.route('/label', methods=['GET', 'POST'])
def label():
    is_pass = True
    username = session.get(USERNAME, '')
    task_id = None
    if session[DEBUG] and session[TASK] == TASK_DOC and session[NEXT_TASK_IDX] == len(session[TASK_IDS]):
        doc_next = get_next_doc(session)
        if doc_next:
            session[DOC_ID] = doc_next[DOC_ID]
            session[TASK_IDS] = load_task_ids(session)
            session[NEXT_TASK_IDX] = 0
    if session[NEXT_TASK_IDX] < len(session[TASK_IDS]):
        task_id = session[TASK_IDS][session[NEXT_TASK_IDX]]
        session[TASK_ID] = task_id
    if not is_pass:
        form = FeedbackForm()
        return render_template('end.html', form=form, code=None,
                               task_url_next=None)
    is_verify = False
    task_data = load_label_tasks(session)
    if session[TASK] == TASK_WRITE:
        session[TURN_ID] = task_data[TURN_ID]
        # task_data['anno_w'] = {ROLE:'user', 'action_desc': 'Ask a question that can be answered by the highlighted text and select your question type.', 'input_text': 'How long is the wait?'}
        if 'anno_w' in task_data:
            is_verify = True
    if task_data is None:
        return redirect(url_for('.end'))
    if ROLE in task_data:
        session[ROLE] = task_data[ROLE]
    task_html = 'task.{}.html'.format(session[TASK])
    if session[TASK] == TASK_LR:
        form = AnnotationLabelRelationForm()
    elif session[TASK] == TASK_LS:
        form = AnnotationLabelForm()
    elif session[TASK] == TASK_WRITE:
        form = AnnotationWriteForm()
    else:
        form = AnnotationDocForm()
    label_ids = []
    if task_data is not None and 'label_ids' in task_data:
        label_ids = task_data['label_ids']
        task_data['doc_info'] = config['metadata']['doc_info']
        if session[TASK] == TASK_LR:
            relation_h = [('is-sibling-unordered', 'is-sibling-of (unordered)'), ('is-sibling-ordered', 'is-sibling-of (ordered)'), ('is-parent-of', 'is-parent-of'), ('is-child-of', 'is-child-of'), ('other', 'other')]
            relation_c = [("is-precondition-of", "is-precondition-of"), ("is-solution-of", "is-solution-of"), ("is-issue-of", "is-issue-of"), ("other", "other")]
            d_choices = {'h': relation_h, 'c': relation_c}
            task_data['choices'] = d_choices
    if session[NEXT_TASK_IDX] < len(session[TASK_IDS]):
        progress = 'task {} {} out of {}'.format(session[TASK], session[NEXT_TASK_IDX] + 1, len(session[TASK_IDS]))
        return render_template(task_html, form=form, label_ids=label_ids, is_debug=session[DEBUG], task_data=task_data,
                                next_task_idx=session[NEXT_TASK_IDX], is_verify=is_verify,
                                username=username, progress=progress)
    else:
        return redirect(url_for('.end'))


@app.route('/end', methods=['GET', 'POST'])
def end():
    form = FeedbackForm()
    task_id = session.get(TASK_ID, '')
    is_pass = True
    n_task = 1
    current_reward = 0
    estimated_reward = 0
    code = None
    if is_pass:
        code = task_id[::-1]
    if request.method == 'POST':
        form = FeedbackForm()
        feedback = form.feedback.data
        session['feedback'] = feedback
        insert_crowd_info(session, {})
        return render_template('end.html', form=form, code=code,
                               n_task=n_task, message=MESSAGE,
                               current_reward=current_reward,
                               estimated_reward=estimated_reward)
    return render_template('end.html', form=form, code=code, n_task=n_task,
                           current_reward=current_reward,
                           estimated_reward=estimated_reward)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = WorkerLoginForm()

    # Extract task ids and task information
    task_ids = request.args.get(TASK_IDS).split(SEP)
    task_id = task_ids[0]

    task = request.args.get(TASK)
    session[TASK] = task

    # If document is specified in request then add that to session
    if DOC_ID in request.args:
        session[DOC_ID] = request.args.get(DOC_ID)

    # Set debug variable
    is_debug = request.args.get('debug')

    if session[TASK] == TASK_WRITE:
        session[ROOM] = task_id

    if form.validate_on_submit():
        if not verify_worker(form.workerid.data):
            # TODO Add logic to terminal task for worker
            pass
        configure_session_for_worker(form.workerid.data, form.username.data, task, task_ids)

        worker_id = session[WORKER_ID]
        session[PASS] = False
        session[DEBUG] = bool(int(is_debug)) if is_debug else False
        if worker_id:
            session[PASS] = is_pass_test(session, worker_id)
        # TODO: Add quiz for label_relation task
        # TODO: Remove fix to bypass quiz for label_relation task.
        if session[TASK] == TASK_LR:
            session[PASS] = True
        if session[PASS]:
            return redirect(url_for('.label'))
        elif session[TASK] == TASK_LS:
            return redirect(url_for('.test'))
    return render_template('index.{}.html'.format(config['domain_name']), form=form, is_debug=is_debug)