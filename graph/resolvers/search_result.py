from dataclasses import dataclass
from typing import NamedTuple

from ariadne import InterfaceType

from graph.graphql import Resolver


def resolve_search_result_type(obj, *_):
    if isinstance(obj, Client):
        return "Client"
    if isinstance(obj, Order):
        return "Order"
    if isinstance(obj, Product):
        return "Product"
    return None


search_result = InterfaceType("SearchResult", resolve_search_result_type)

Resolver(search_result)

resolver = Resolver(search_result)


@resolver
def summary(obj, *_):
    return str(obj)


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
