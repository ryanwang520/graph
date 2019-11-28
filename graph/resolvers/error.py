from ariadne import UnionType

from graph.graphql import Resolver


def resolve_error_type(obj, *_):
    if obj.get("code"):
        return "AccessError"
    return "NotFoundError"


error = UnionType("Error", resolve_error_type)

Resolver(error)
