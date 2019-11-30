from graph.graphql import ObjectTypeResolver

resolver = ObjectTypeResolver("Mutation")


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
