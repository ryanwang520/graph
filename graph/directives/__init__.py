from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver

# TODO
# LengthDirective, 验证长度
# directive @ length(max: Int) on FIELD_DEFINITION | INPUT_FIELD_DEFINITION

# uniqueID


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
