from graph.graphql import ObjectTypeResolver
from graph.models import User

resolver = ObjectTypeResolver("User")

resolver.set_alias("name", "fullname")


@resolver
def user_name(*_):
    return "resolved user name"


@resolver
def search(*_):
    from graph.resolvers.search_result import Client

    return Client(first_name="client")


@resolver
def followers(*_):
    return {"total": 10, "items": [User(user_name="first", id=2, name="n",)]}


@resolver
def parent(*_, level):
    return f"parent {level}"


@resolver
def status(*_):
    return 1
