from ariadne import MutationType


class ApiException(Exception):
    def __init__(self, message):
        self.message=  message

mutation = MutationType()
@mutation.field('login')
def resolve_login(obj, info, input):
    # raise ApiException('login failed')
    print(type(input.get('time')))
    print(input['username'])
    return {"status": True}

