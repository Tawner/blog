import hashlib, random, string
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


def md5(content):
    """
    md5加密函数
    :param content: [str|bytes] 要加密的内容
    :return:
    """
    res = hashlib.md5(content).hexdigest() if isinstance(content, bytes) else hashlib.md5(content.encode()).hexdigest()
    return res


def random_str(length):
    """
    生成随机字符串
    :param length: [int] 长度
    :return:
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def encrypt(data, expire=7*86400):
    """
    字典生成加密字符串函数
    :param data [dict] 需要加密的数据
    :param expire [int] 过期时间单位秒
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=expire)
    return s.dumps(data).decode("ascii")


def decrypt(encrypt_str):
    """
    解密函数
    :param encrypt_str [str] 要解密的字符串
    :return:
    """
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(encrypt_str)
    except Exception:
        return None
    return data


