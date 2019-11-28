from graph.graphql import Type
from graph.models import User

query = Type('Query')


@query
def viewer(_, info):
    print(info.context)

    return User(name='moon shadow', user_name='un', id=123, image=dict(
        sm='a',
        md='b',
        lg='c'
    ))


@query
def test_union(*_):
    return {"code": 1}


@query
def bindable(*_):
    return 'hello'
