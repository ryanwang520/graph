import datetime
from dataclasses import dataclass



@dataclass
class User:
    id: int
    name: str
    user_name: str
    image: dict = None

    def parent(self, info, level):
        return f'parent {level}'

    def age(self, info):
        return 12

    def fullname(self, info):
        return 'full name'

    def created_at(self, info):
        return datetime.datetime.utcnow()

    def status(self, info):
        from .app import UserStatus
        return UserStatus.ACTIVE

    def search(self, info):
        from .app import Client
        return Client(first_name='client')

    def followers(self, info):
        return {'total':10, 'items':[User(user_name='first', id=2, name='n',)]}
