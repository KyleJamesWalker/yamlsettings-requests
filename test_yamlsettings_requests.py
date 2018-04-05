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
def test_load(resps, url, obj):
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
