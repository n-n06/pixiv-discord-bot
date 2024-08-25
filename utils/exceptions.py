'''
Some helpful exceptions
'''

class IllustrationNotFound(Exception):
    def __init__(self):
        super().__init__('Illustration Not Found')


class IllustrationInvinsible(Exception):
    def __init__(self):
        super().__init__('Illustration Set to Invinsible')
