from ariadne import ObjectType

from graph.model import User

user = ObjectType("User")

user.set_alias("name", "fullname")


@user.field("userName")
def user_name(*_):
    return 'resolved user name'

@user.field("search")
def search(*_):
    from graph.app import Client
    return Client(first_name='client')

@user.field("followers")
def followers(self, info):
    return {'total':10, 'items':[User(user_name='first', id=2, name='n',)]}

@user.field("parent")
def parent(self, info, level):
    return f'parent {level}'
