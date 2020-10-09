from flask_restful import reqparse, abort
from common.libs import inputs


# 排期相关校验
class BaseParse:
    def __init__(self):
        self.parse = reqparse.RequestParser()
        self.params = {}

    def parse_args(self):
        self.add_arguments()
        req_val = self.parse.parse_args()
        for key, val in req_val.items():
            if val is not None:
                self.params[key] = val
        self.other_parse()
        return self.params

    def add_arguments(self):  # 参数添加
        pass

    def other_parse(self):  # 其他校验
        pass

