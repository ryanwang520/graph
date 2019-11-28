import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    user_name: str
    image: dict = None

    @property
    def age(self):
        return 12

    @property
    def fullname(self):
        return 'full name'

    @property
    def created_at(self):
        return datetime.datetime.utcnow()

    @property
    def status(self, ):
        return "ACTIVE"
