from ariadne import ObjectType

from graph.graphql import Resolver

pet = ObjectType("Pet")

resolver = Resolver(pet)


@resolver
def name(*_):
    return "pet x"
