from graph.graphql import Type
from graph.models import User

user = Type("User")

user.set_alias("name", "fullname")


@user
def user_name(*_):
    return 'resolved user name'


@user
def search(*_):
    from graph.resolvers.search_result import Client
    return Client(first_name='client')


@user
def followers(*_):
    return {'total': 10, 'items': [User(user_name='first', id=2, name='n', )]}


@user
def parent(*_, level):
    return f'parent {level}'
