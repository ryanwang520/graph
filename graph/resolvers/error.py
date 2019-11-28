from ariadne import UnionType

error = UnionType("Error")


@error.type_resolver
def resolve_error_type(obj, *_):
    if obj.get("code"):
        return "AccessError"
    return "NotFoundError"
