from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer


class Serializer(object):
    def init_app(self, app):
        self.secret_key = app.config['SECRET_KEY']
        self.salt = app.config['SECURITY_PASSWORD_SALT']
        self.s = self.get_serializer()
        self.ts = self.get_timed_serializer()

    def get_serializer(self):
        return URLSafeSerializer(self.secret_key)

    def get_timed_serializer(self):
        return URLSafeTimedSerializer(self.secret_key)

    def serialize_data(self, data):
        return self.s.dumps(data, salt=self.salt)

    def serialize_timed_data(self, data):
        return self.ts.dumps(data, salt=self.salt)

    def load_token(self, token):
        return self.s.loads(token, salt=self.salt)

    def load_timed_token(self, token, expiration=3600):
        return self.ts.loads(token, salt=self.salt, max_age=expiration)
