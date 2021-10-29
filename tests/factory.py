from unittest.mock import Mock

class CommandParserFactory(object):
    @staticmethod
    def create_args(*args, **kwargs):
        a = Mock()
        for k,v in kwargs.items():
            setattr(a,f"{k}",v)
        return a
