from ariadne import (
    ObjectType,
    graphql_sync,
    snake_case_fallback_resolvers,
    make_executable_schema,
    InterfaceType,
)
from ariadne.constants import PLAYGROUND_HTML
from flask import jsonify, request, Flask

from graph.helpers import convert_snake_case_to_camel


class Resolver:
    resolvers = []

    def __init__(self, type_obj):
        self.resolver = type_obj
        Resolver.resolvers.append(self.resolver)


class ObjectTypeResolver(Resolver):
    def __init__(self, name_or_obj_type):
        if isinstance(name_or_obj_type, str):
            resolver = ObjectType(name_or_obj_type)
        else:
            resolver = name_or_obj_type
        super().__init__(resolver)

    def set_alias(self, name, to):
        self.resolver.set_alias(name, to)

    def field(self, name_or_fn):
        if not hasattr(self.resolver, "field"):
            raise AttributeError("resolver type has no `field` attribute")
        if isinstance(name_or_fn, str):
            return self.resolver.field(name_or_fn)

        fn = name_or_fn

        fn_name = fn.__name__

        return self.resolver.field(convert_snake_case_to_camel(fn_name))(fn)

    def __call__(self, *args, **kwargs):
        return self.field(*args, **kwargs)


class InterfaceResolver(ObjectTypeResolver):
    def __init__(self, name, type_resolver):
        resolver = InterfaceType(name, type_resolver)
        super().__init__(resolver)


def create_server(
    type_defs, resolvers, directives=None, extensions=None, error_formatter=None
):
    schema = make_executable_schema(
        type_defs, *resolvers, snake_case_fallback_resolvers, directives=directives,
    )
    app = Flask(__name__)

    @app.route("/graphql", methods=["GET"])
    def graphql_playgroud():
        return PLAYGROUND_HTML, 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()

        success, result = graphql_sync(
            schema,
            data,
            debug=app.debug,
            context_value=None,
            error_formatter=error_formatter,
            extensions=extensions,
        )

        status_code = 200 if success else 400
        return jsonify(result), status_code

    return app
