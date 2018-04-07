import yamlsettings
import pytest
import responses

from requests.auth import HTTPBasicAuth


@pytest.fixture
def resps():
    """Mock request fixture"""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.mark.parametrize(
    "url,obj",
    [
        ('http://testing.com/foobar', {'test': 'win'}),
        ('http://testing.com:90/foobar', {'test': 'win'}),
        ('http://test@testing.com/foobar', {'test': 'win'}),
        ('http://test@testing.com:60/foobar', {'test': 'win'}),
        ('http://test:foo@testing.com/foobar', {'test': 'win'}),
        ('http://test:foo@testing.com:99/foobar', {'test': 'win'}),
        ('http://test:foo@testing.com:99/foobar', {'test': 'win'})
    ],
)
def test_user_pass_combos(resps, url, obj):
    """Test loading with u/p urls"""
    resps.add(responses.GET, url,
              json=obj, status=200)

    config = yamlsettings.load(url)
    assert config.test == obj['test']


def test_fail_first_load(resps):
    url_bad = 'https://bad_times.com/not_found'
    url_good = 'https://good_times.com/happy_page'
    resps.add(responses.GET, url_bad,
              body='Page Not Found', status=404)
    resps.add(responses.GET, url_good,
              body='{"happy": True}', status=200)

    config = yamlsettings.load([url_bad, url_good])
    assert config.happy is True


def test_auth_required(resps):
    url = "https://verysecure.com/doc"
    resps.add(responses.GET, url,
              body='{"secure": true}', status=200)
    config = yamlsettings.load(
        url,
        auth=HTTPBasicAuth('Aladdin', 'OpenSesame'),
    )
    auth_header = resps.calls[0].request.__dict__['headers']['Authorization']
    assert auth_header == "Basic QWxhZGRpbjpPcGVuU2VzYW1l"
    assert config.secure is True


def test_no_raise_with_unexpected(resps):
    """Test Runtime Error when excepted status code"""
    url_1 = 'http://testing.com/one'
    url_2 = 'http://testing.com/two'
    expected = 202
    raise_on = False

    resps.add(responses.GET, url_1, json={'error': True}, status=500)
    resps.add(responses.GET, url_2, json={'foo': 'bar'}, status=202)

    config = yamlsettings.load([url_1, url_2],
                               expected_status_code=expected,
                               raise_on_status=raise_on)
    assert config.foo == 'bar'


def test_raise_with_unexpected(resps):
    """Test Runtime Error when excepted status code"""
    url = 'http://testing.com/one'
    obj = {'error': True}
    expected = 200
    status = 500
    raise_on = True

    resps.add(responses.GET, url, json=obj, status=status)

    # RuntimeError stops yamlsettings from trying the next url
    with pytest.raises(RuntimeError):
        yamlsettings.load(url,
                          expected_status_code=expected,
                          raise_on_status=raise_on)


def test_not_found_ok(resps):
    """Test 404 can return data when expected"""
    url = 'http://missing.com/data'
    obj = {'hidden': 'treasure'}
    expected = 404
    status = 404

    resps.add(responses.GET, url, json=obj, status=status)
    config = yamlsettings.load(url, expected_status_code=expected)
    assert config.hidden == 'treasure'
