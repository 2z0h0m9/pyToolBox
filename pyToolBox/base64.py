import base64


def encode(data: str):
    """
    this is a func to encode data
    这是一个用来加密数据的函数
    :param data: 待加密数据
    :return: 已加密数据
    """
    return base64.b64encode(data)


def decode(data: str):
    """
    this is a func to decode data
    这是一个用来解密数据的函数
    :param data: 待解密数据
    :return: 已解密数据
    """
    return base64.b64decode(data)
