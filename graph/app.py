import os

from ariadne import load_schema_from_path, format_error
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtensionSync
from graphql import GraphQLError

from graph.directives import PermissionDirective
from graph.extensions import QueryExecutionTimeExtension
from graph.graphql import create_server, Resolver
from graph.helpers import preload_module, ApiException

type_defs = load_schema_from_path(os.path.join(os.path.dirname(__file__), "schema"))

preload_module("graph.resolvers")
preload_module("graph.mutations")

resolvers = Resolver.resolvers

directives = {"needsPermission": PermissionDirective}
extensions = [ApolloTracingExtensionSync, QueryExecutionTimeExtension]


def error_formatter(error: GraphQLError, debug: bool = False) -> dict:
    if not debug:
        if isinstance(error.original_error, GraphQLError) and isinstance(
            error.original_error.original_error, ApiException
        ):
            formatted = error.formatted
            formatted["message"] = error.original_error.original_error.message
            return formatted
    return format_error(error, debug)


app = create_server(type_defs, resolvers, directives, extensions, error_formatter)
