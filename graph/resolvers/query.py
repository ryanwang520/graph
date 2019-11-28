from ariadne import QueryType

from graph.graphql import Resolver
from graph.models import User

query = QueryType()

resolver = Resolver(query)


@resolver
def viewer(_, info):
    print(info.context)

    return User(
        name="moon shadow", user_name="un", id=123, image=dict(sm="a", md="b", lg="c")
    )


@resolver
def test_union(*_):
    return {"code": 1}


@resolver
def bindable(*_):
    return "hello"


@resolver
def pet(*_):
    return {"name": "pet"}
