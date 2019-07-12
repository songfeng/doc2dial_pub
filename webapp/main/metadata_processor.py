from wtforms.fields import (StringField, RadioField, SelectField,
                            SelectMultipleField, IntegerField, FloatField)
from .const import (NAME, DATA_TYPE, BOOLEAN, TEXT, STRING, INTEGER, FLOAT,
                    HAS_RANGE, HAS_VALUES, IS_MULTIPLE)


def metadata2form(d_meta):
    '''
    DataType: Boolean, Date, DateTime, Number, Text, Time
    HAS_RANGE: low / high
    '''
    name = d_meta[NAME] if NAME in d_meta else 'default'
    data_type = d_meta[DATA_TYPE] if DATA_TYPE in d_meta else STRING
    d_func = {STRING: StringField.__name__, INTEGER: IntegerField.__name__,
              FLOAT: FloatField.__name__, TEXT: StringField.__name__,
              BOOLEAN: RadioField.__name__}
    func = d_func[data_type] if data_type in d_func else 'StringField'
    if HAS_RANGE in d_meta and d_meta[HAS_RANGE]:
        return [(func, {NAME: name + '_high'}), (func, {NAME: name + '_low'})]
    choices = None
    if HAS_VALUES in d_meta and d_meta[HAS_VALUES]:
        if IS_MULTIPLE in d_meta:
            choices = [(None, 'None')]
            values = d_meta[HAS_VALUES]
            if d_meta[IS_MULTIPLE]:
                func = SelectMultipleField.__name__
            else:
                func = SelectField.__name__
            choices += [(e, str(e)) for e in values]
    return [(func, {'choices': choices, NAME: name})]


def metadata_valuetype(lst_meta):
    lst_single_value = []
    lst_multiple_value = []
    for ele in lst_meta:
        for key, d_meta in ele.items():
            data_type = d_meta[DATA_TYPE]
            if IS_MULTIPLE in d_meta:
                if d_meta[IS_MULTIPLE]:
                    if HAS_RANGE in d_meta:
                        lst_multiple_value.append((key + '_low', data_type))
                        lst_multiple_value.append((key + '_high', data_type))
                    else:
                        lst_multiple_value.append((key, data_type))
                else:
                    if HAS_RANGE in d_meta:
                        lst_single_value.append((key + '_low', data_type))
                        lst_single_value.append((key + '_high', data_type))
                    else:
                        lst_single_value.append((key, data_type))
    return lst_single_value, lst_multiple_value
