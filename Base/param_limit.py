from SmartDjango import ModelError


class ParamLimit:
    @staticmethod
    def str_len(max_len, min_len=0):
        def decorator(string):
            if not isinstance(string, str):
                raise ModelError.FIELD_FORMAT
            if len(string) < min_len or len(string) > max_len:
                raise ModelError.FIELD_FORMAT
        return decorator

    @staticmethod
    def choices(choices):
        def decorator(value):
            if value not in choices:
                raise ModelError.FIELD_FORMAT
        return decorator

    @staticmethod
    def number(max_, min_=0):
        def decorator(value):
            if value > max_:
                value = max_
            if value < min_:
                value = min_
            return value
        return decorator


PL = ParamLimit
