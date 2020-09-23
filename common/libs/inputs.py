from flask_restful.inputs import *
from common.models.upload import *


def _get_string(value):
    if isinstance(value, str): return value
    else: raise ValueError('{0} is not a valid string'.format(value))


def _get_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError('{0} is not a valid integer'.format(value))


class str_range(object):
    """字符串长度"""
    def __init__(self, low, high, argument='argument'):
        self.low = low
        self.high = high
        self.argument = argument

    def __call__(self, value):
        value = _get_string(value)
        if len(value) < self.low or len(value) > self.high:
            error = ('Invalid {arg}: {val}. {arg} length must be within the range {lo} - {hi}'
                     .format(arg=self.argument, val=value, lo=self.low, hi=self.high))
            raise ValueError(error)
        return value


class date_time:
    """时间格式化"""
    def __init__(self, time_format='%Y-%m-%d', argument='argument'):
        self.time_format = time_format
        self.argument = argument

    def __call__(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        elif isinstance(value, str):
            try:
                value = datetime.strptime(value, self.time_format)
            except:
                return ValueError(self.argument + '参数格式错误')
            return value
        else:
            raise ValueError(self.argument + '参数格式错误')


class data_exist:
    """数据存在判断"""
    def __init__(self, model, re_obj=False, argument='argument'):
        self.model = model
        self.argument = argument
        self.re_obj = re_obj

    def __call__(self, value):
        value = _get_integer(value)
        obj = self.model.query.filter(self.model.id == value, self.model.is_delete == 0).first()
        if not obj: raise ValueError(self.argument + '参数错误，数据不存在')
        return obj if self.re_obj else value