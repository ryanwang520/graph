from ariadne import MutationType

from graph.graphql import Resolver


class ApiException(Exception):
    def __init__(self, message):
        self.message = message


mutation = MutationType()

resolver = Resolver(mutation)


@resolver
def login(*_, input, a=None):
    print(a)
    print(type(input.get("time")))
    print(input["username"])
    return {"status": True}


@resolver
def logout(*_, n=None):
    print(n)
    return {"status": False}
