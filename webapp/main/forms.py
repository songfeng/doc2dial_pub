from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, SubmitField, RadioField, SelectField,
                            SelectMultipleField, IntegerField, FloatField,
                            TextAreaField)
from wtforms.validators import DataRequired
from wtforms import widgets
from ..main.const import *  
from .metadata_processor import metadata2form
from .. import config


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class AdminLoginForm(FlaskForm):
    default_task_choice = TASK_WRITE  # TASK_LS TASK_WRITE TASK_LR
    default_document = ''
    if config['domain_name'] == 'demo':
        default_document = 'devices_at_worksystem'  # 'access_cloud_mail' # 'aix' #
    document = StringField('document', id='document', default=default_document)
    username = StringField('username', id="username", validators=[DataRequired()])
    password = PasswordField('password', id="password", validators=[DataRequired()])
    task_ids = StringField('task_ids', id="task_ids", validators=None)
    role = RadioField('role', choices=[('user', 'user'), ('agent', 'agent')],
                      validators=[DataRequired()], default='user')
    mode = RadioField('mode', choices=[('anno_label', 'anno with labels'), ('anno_question', 'anno with questions')],
                      validators=[DataRequired()], default='anno_label')
    task_choices = [(ele, ele.replace('_', ' ')) for ele in config['metadata']['tasks']]
    task = RadioField('task', choices=task_choices, validators=[DataRequired()], default=default_task_choice)
    submit = SubmitField('Start', id='login')


class WorkerLoginForm(FlaskForm):
    workerid = StringField('worderid', id='workerid', validators=[DataRequired()])
    username = StringField('username', id="username", validators=[DataRequired()])
    submit = SubmitField('Start', id='login')


class AnnotationLabelForm(FlaskForm):
    submit = SubmitField('Save', id='save')


class AnnotationLabelRelationForm(FlaskForm):
    choices_hierarchical = [('is-sibling-unordered', 'is-sibling (unordered)'), ('is-sibling-ordered', 'is-sibling (ordered)'), ('is-parent-of', 'is-parent-of'), ('is-child-of', 'is-child-of'), ('other', 'other')]
    relation_h = RadioField('relation_h', choices=choices_hierarchical, validators=[DataRequired()], default='other')
    choices_content = [("is-precondition-of", "is-precondition-of"), ("is-solution-of", "is-solution-of"), ("is-issue-of", "is-issue-of"), ("other", "other")]
    relation_c = RadioField('relation_c', choices=choices_content, validators=[DataRequired()], default='other')
    submit = SubmitField('Save', id='save')


class AnnotationDocForm(FlaskForm):
    d_func = {'IntegerField': IntegerField, 'StringField': StringField,
              'FloatField': FloatField, 'RadioField': RadioField, 
              'SelectField': SelectField,
              'SelectMultipleField': SelectMultipleField}
    for d_meta in config["metadata"][TASK_DOC]:
        for func, d in metadata2form(list(d_meta.items())[0][-1]):
            if func in ['SelectField', 'SelectMultipleField']:
                tmp = d_func[func](d[NAME], choices=d['choices'], id=d[NAME])
            else:
                tmp = d_func[func](d[NAME], id=d[NAME])
            exec(d[NAME] + ' = tmp')
    suggest = RadioField('suggest', choices=[('no', 'Probably No'), ('no-', 'Maybe No'), ('yes-', 'Maybe Yes'), ('yes', 'Probaby Yes')],
                      validators=[DataRequired()], default='No')
    submit = SubmitField('Save', id='save')


class AnnotationWriteForm(FlaskForm):
    d_func = {'IntegerField': IntegerField, 'StringField': StringField,
              'FloatField': FloatField, 'SelectField': SelectField,
              'SelectMultipleField': SelectMultipleField}
    for d_meta in config["metadata"][TASK_WRITE]:
        for func, d in metadata2form(list(d_meta.items())[0][-1]):
            if func in ['SelectField', 'SelectMultipleField']:
                tmp = d_func[func](d[NAME], choices=d['choices'], id=d[NAME])
            else:
                tmp = d_func[func](d[NAME], id=d[NAME])
            exec(d[NAME] + ' = tmp')
    approval = RadioField('approval', choices=[('no', 'Probably No'), ('no-', 'Maybe No'), ('yes-', 'Maybe Yes'), ('yes', 'Probaby Yes')],
                      validators=[DataRequired()], default='No')
    submit = SubmitField('Save', id='save')


class ResultForm(FlaskForm):
    label_choices = [('P', 'Precondition(P)'), ('S', 'Solution(S)'), ('B', 'Both(B)'), ('O', 'Other(O)')]
    q1 = RadioField('q1', choices=label_choices, validators=[DataRequired()], default="P")
    q2 = RadioField('q2', choices=label_choices, validators=[DataRequired()], default="S")
    q3 = RadioField('q3', choices=label_choices, validators=[DataRequired()], default="B")
    q4 = RadioField('q4', choices=label_choices, validators=[DataRequired()], default="P")
    q5 = RadioField('q4', choices=label_choices, validators=[DataRequired()], default="S")
    q6 = RadioField('q4', choices=label_choices, validators=[DataRequired()], default="P")
    submit = SubmitField('Submit', id='test_submit')


class TestForm(FlaskForm):
    yes_no_choices = [('yes', 'Yes'), ('no', 'No'), ('other', 'Not sure')]
    label_choices = [('P', 'Precondition(P)'), ('S', 'Solution(S)'), ('B', 'Both(B)'), ('O', 'Other(O)')]
    q1 = RadioField('q1', choices=label_choices, validators=[DataRequired()], default="O")
    q2 = RadioField('q2', choices=label_choices, validators=[DataRequired()], default="O")
    q3 = RadioField('q3', choices=label_choices, validators=[DataRequired()], default="O")
    q4 = RadioField('q4', choices=label_choices, validators=[DataRequired()], default="O")
    q5 = RadioField('q4', choices=label_choices, validators=[DataRequired()], default="O")
    q6 = RadioField('q4', choices=label_choices, validators=[DataRequired()], default="O")
    submit = SubmitField('Submit', id='test_submit')


class FeedbackForm(FlaskForm):
    feedback = TextAreaField('feedback', id='feedback',
                             validators=[DataRequired()])
    submit = SubmitField('Submit', id='feedback_submit')
