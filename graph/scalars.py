from dateutil import parser

from ariadne import ScalarType


def serialize_datetime(value):
    return value.isoformat()


def parse_datetime_value(value):
    if value:
        return parser.parse(value)


datetime_scalar = ScalarType(
    "Datetime", serializer=serialize_datetime, value_parser=parse_datetime_value)
