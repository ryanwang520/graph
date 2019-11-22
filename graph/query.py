from ariadne import QueryType, ObjectType

from graph.model import User

query = QueryType()
@query.field("viewer")
def resolve_viewer(*_):
    return User(name='moon shadow', user_name='un', id=123, image=dict(
        sm='a',
        md='b',
        lg='c'
    ))


@query.field("testUnion")
def resolve_union(*_):
    return {"code": 1}

@query.field("bindable")
def resolve_bindable(*_):
    return 'hello'

user = ObjectType("User")

user.set_alias("name", "fullname")

@user.field("userName")
def _(*_):
    return 'resolved user name'



