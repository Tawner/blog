from flask_restful import reqparse, abort
from common.libs import inputs


# 排期相关校验
class BaseParse:
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.params = {}

    def parse_args(self):
        self.add_arguments()
        self.params = self.parse.parse_args()
        self.other_parse()
        req_val = {}
        for key, val in self.params.items():
            if val is not None:
                req_val[key] = val
        return req_val

    def add_arguments(self):  # 参数添加
        pass

    def other_parse(self):  # 其他校验
        pass

