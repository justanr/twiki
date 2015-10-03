from twiki import factory

try:
    from unittest import mock
except ImportError:
    import mock


def test_find_app_config_with_no_name():
    with mock.patch('twiki.factory.get_config_from_env') as environ:
        factory.find_app_config()

    assert environ.call_args == mock.call(default='default')


def test_config_app():
    app = mock.MagicMock()

    factory.config_app(app, 'dev')

    assert app.config.from_object.call_count == 2
    assert app.config.__setitem__.call_args == mock.call('CONFIG_NAME', 'DevConfig')
