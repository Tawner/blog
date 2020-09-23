from flask_restful.fields import *
import six


class MarshallingException(Exception):
    """
    This is an encapsulating Exception in case of marshalling error.
    """

    def __init__(self, underlying_exception):
        # just put the contextual representation of the error to hint on what
        # went wrong without exposing internals
        super(MarshallingException, self).__init__(six.text_type(underlying_exception))


class Datetime(Raw):
    """时间格式化"""
    def __init__(self, dt_format='%Y-%m-%d', **kwargs):
        super(Datetime, self).__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        try:
            return value.strftime(self.dt_format)
        except AttributeError as ae:
            raise MarshallingException(ae)
