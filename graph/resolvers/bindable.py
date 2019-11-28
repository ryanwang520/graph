from ariadne import SchemaBindable
from graphql import GraphQLSchema

from graph.graphql import Resolver


class Bindable(SchemaBindable):
    def __init__(self, name):
        self.name = name

    def bind_to_schema(self, schema: GraphQLSchema) -> None:
        graphql_type = schema.type_map.get(self.name)
        graphql_type.fields["first"].resolve = lambda *_: "first bind"
        graphql_type.fields["second"].resolve = lambda *_: "second bind"


bindable = Bindable("Bind")

Resolver(bindable)
