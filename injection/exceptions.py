class InjectionKeyError(BaseException):
    def __init__(self, msg):
        BaseException.__init__(msg)
