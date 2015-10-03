class BaseConfig(object):
    @classmethod
    def init_app(cls, app):
        app.config['CONFIG_NAME'] = cls.__name__


class DevConfig(BaseConfig):
    SECRET_KEY = 'fred'
    DEBUG = True


class TestConfig(BaseConfig):
    SECRET_KEY = 'fred'
    TESTING = True


class ProdConfig(BaseConfig):
    SECRET_KEY = 'fred'


DefaultConfig = ProdConfig


configs = {'dev': DevConfig,
           'test': TestConfig,
           'prod': ProdConfig}
