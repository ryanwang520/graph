from graph.graphql import ObjectTypeResolver

resolver = ObjectTypeResolver("Pet")


@resolver
def name(*_):
    return "pet x"
