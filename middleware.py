from datetime import date

# front controllers:

def secret_front(request):
    request['date'] = f'{date.today()}'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
