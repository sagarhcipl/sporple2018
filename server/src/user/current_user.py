from flask.ext.login import AnonymousUserMixin


class CurrentUser:
    def __init__(self, user):
        self.userid = user.id
        self.authenticated = True
        self.active = user.is_active
        self.anonymous = False
        self.user = user

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return self.userid

    def get_name(self):
        return self.user.name

    def get_locale(self):
        return 'en_US'


class Anonymous(AnonymousUserMixin):
    def get_locale(self):
        return 'en_US'
