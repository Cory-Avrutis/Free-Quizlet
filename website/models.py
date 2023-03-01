from flask_login import UserMixin

class User:
    def __init__(self,username):
        self.username = username
    
    @staticmethod
    def is_authenticated():
        return True
    
    @staticmethod
    def is_active():
        return True
    
    @staticmethod
    def is_anonymous():
        return True

    def get_id(self):
        return self.username

