from ariadne import EnumType

from graph.graphql import Resolver

# 一般不需要在绑定达到另一个value了
user_status = EnumType("UserStatus", {"STANDARD": 1, "PINNED": 2, "PROMOTED": 3,},)

Resolver(user_status)
