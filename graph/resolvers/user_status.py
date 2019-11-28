from ariadne import EnumType

from graph.graphql import Resolver

user_status = EnumType("UserStatus", {"STANDARD": 1, "PINNED": 2, "PROMOTED": 3,},)

Resolver(user_status)
