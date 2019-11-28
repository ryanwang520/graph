from graph.graphql import Type


class ApiException(Exception):
    def __init__(self, message):
        self.message = message


mutation = Type('Mutation')


@mutation
def login(*_, input, a=None):
    print(a)
    print(type(input.get('time')))
    print(input['username'])
    return {"status": True}
