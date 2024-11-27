
class User:
    def __init__(self, id=None, owner_name=None, email=None, owner_password=None):
        self._id = id
        self._name = owner_name
        self._email = email
        self._password = owner_password

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, owner_name):
        self._name = owner_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, owner_password):
        self._password = owner_password


