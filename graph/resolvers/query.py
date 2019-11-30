from graph.graphql import ObjectTypeResolver
from graph.models import User

resolver = ObjectTypeResolver("Query")


@resolver
def viewer(_, info):
    print(info.context)

    return User(
        name="moon shadow", user_name="un", id=123, image=dict(sm="a", md="b", lg="c")
    )


@resolver
def error(*_):
    return {"code": 1}


@resolver
def bindable(*_):
    return "hello"


@resolver
def pet(*_):
    return {"name": "pet"}
