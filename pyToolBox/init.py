import elevate


def self_reported():
    print('''
        you can use this warehouse to do:
            1.encryption and decryption Base64 code
            2.elevate privileges(applying administrator rights on windows, macOS or linux)
            3.make gif files
        这个库可以:
            1.加解密Base64
            2.提权(可以在windows, macOS和linux上使用)
            3.制作GIF文件
        ''')


def authority():
    """
    this is a func to elevate privileges
    这个函数用来提升权限
    :return: 无
    """
    elevate.elevate()
