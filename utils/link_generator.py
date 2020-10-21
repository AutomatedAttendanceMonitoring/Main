from datetime import datetime, timezone
from dataclasses import dataclass
from hashlib import sha1

@dataclass
class LinkGenerator:

    @staticmethod
    def get_link(model=None, **kwargs):
        data = (LinkGenerator.get_arguments(**model.__dict__) if model else "") + \
               datetime.now(timezone.utc).__str__() + \
               LinkGenerator.get_arguments(**kwargs)

        link = sha1(data.encode('utf-8'))
        return link.hexdigest()

    @staticmethod
    def get_arguments(**kwargs):
        res = ""
        if kwargs:
            for i in kwargs:
                res = res + i
        return res
