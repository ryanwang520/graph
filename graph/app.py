import enum
from ariadne.types import ExtensionSync as Extension, SchemaBindable, SchemaBindable
import os
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtensionSync
import time

from dataclasses import dataclass
from typing import NamedTuple

from dateutil import parser
from ariadne import (
    graphql_sync,
    make_executable_schema,
    load_schema_from_path,
    snake_case_fallback_resolvers,
    format_error,
    ScalarType,
    EnumType,
    UnionType,
    InterfaceType,
    SchemaDirectiveVisitor,
)
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from graphql import GraphQLError, default_field_resolver, GraphQLSchema

from graph.mutations import mutation, ApiException
from graph.query import query
from graph.resolvers.user import user

base = os.path.dirname(__file__)
type_defs = load_schema_from_path(os.path.join(base, "schema"))


def serialize_datetime(value):
    return value.isoformat()


def parse_datetime_value(value):
    if value:
        return parser.parse(value)


datetime_scalar = ScalarType(
    "Datetime", serializer=serialize_datetime, value_parser=parse_datetime_value
)

# class UserStatus(enum.IntEnum):
#     ACTIVE = 1
#     INACTIVE = 2
#     BANNED = 3


# user_status = EnumType("UserStatus", UserStatus)

error = UnionType("Error")


@error.type_resolver
def resolve_error_type(obj, *_):
    if obj.get("code"):
        return "AccessError"
    return "NotFoundError"


class Client(NamedTuple):
    first_name: str = None
    last_name: str = None
    summary: str = None
    url: str = None


@dataclass
class Order:
    ref: str = None
    client: str = None
    summary: str = None
    url: str = None


@dataclass
class Product:
    name: str = None
    sku: str = None
    summary: str = None
    url: str = None


search_result = InterfaceType("SearchResult")


@search_result.type_resolver
def resolve_search_result_type(obj, *_):
    if isinstance(obj, Client):
        return "Client"
    if isinstance(obj, Order):
        return "Order"
    if isinstance(obj, Product):
        return "Product"
    return None


@search_result.field("summary")
def resolve_summary(obj, *_):
    return str(obj)


class PermissionDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        permission = self.args.get("permission")
        original_resolver = field.resolve or default_field_resolver

        def resolve_formatted_date(obj, info, **kwargs):
            print(permission)
            result = original_resolver(obj, info, **kwargs)
            return result

        field.resolve = resolve_formatted_date
        return field


class Bindable(SchemaBindable):
    def __init__(self, name):
        self.name = name

    def bind_to_schema(self, schema: GraphQLSchema) -> None:
        graphql_type = schema.type_map.get(self.name)
        graphql_type.fields["first"].resolve = lambda *_: "first bind"
        graphql_type.fields["second"].resolve = lambda *_: "second bind"


bindable = Bindable("Bind")

app = Flask(__name__)


class QueryExecutionTimeExtension(Extension):
    def __init__(self):
        self.start_timestamp = None
        self.end_timestamp = None

    def request_started(self, context):
        self.start_timestamp = time.perf_counter_ns()

    def format(self, context):
        return {"execution": time.perf_counter_ns() - self.start_timestamp}


def create_server(type_defs, resolvers, directives, extensions, error_formatter=None):
    schema = make_executable_schema(
        type_defs,
        *resolvers, snake_case_fallback_resolvers,
        directives=directives,
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


# 不要一个一个的加到list里面
resolvers = [
    query,
    user,
    bindable,
    error,
    search_result,
    datetime_scalar,
    mutation]
directives = {"needsPermission": PermissionDirective, }

extensions = [ApolloTracingExtensionSync, QueryExecutionTimeExtension]


def error_formatter(error: GraphQLError, debug: bool = False) -> dict:
    if not debug:
        if isinstance(error.original_error, GraphQLError) and isinstance(
            error.original_error.original_error, ApiException
        ):
            formatted = error.formatted
            formatted["message"] = error.original_error.original_error.message
            return formatted

    # If debug is enabled, reuse Ariadne's formatting logic (not required)
    return format_error(error, debug)


app = create_server(type_defs, resolvers, directives, extensions, error_formatter)
