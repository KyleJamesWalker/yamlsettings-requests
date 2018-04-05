import requests
import urllib
from yamlsettings.extensions.base import YamlSettingsExtension

# Example URL:
# https://gist.githubusercontent.com/elizazhang/1b31cf2cb8b36799a4a231e9d47743c3/raw/95aa81307f9363f3e8d0542848fc4675a2bd6b9c/sample.yaml


class RequestsExtension(YamlSettingsExtension):
    """Open URLs with the request library

    """
    protocols = ['http', 'https']
    # default_query = {
    #     'expected_status_code': "200",
    #     'raise_on_status': "true",
    # }

    @classmethod
    def conform_query(cls, query):
        """Don't conform the query, must pass as received"""
        return query

    @staticmethod
    def rebuild_url(scheme, path, fragment, username,
                    password, hostname, port, query):
        # Rebuild the netloc value
        netloc = "@".join(filter(None, [
            ":".join(
                filter(None, [
                    username,
                    password,
                ])
            ),
            ":".join(
                filter(None, [
                    hostname,
                    str(port or ''),
                ])
            )
        ]))

        return urllib.parse.urlunsplit([
            scheme,
            netloc,
            path,
            query,
            fragment,
        ])

    @classmethod
    def load_target(cls, scheme, path, fragment, username,
                    password, hostname, port, query,
                    load_method, **kwargs):
        url = cls.rebuild_url(scheme, path, fragment, username,
                              password, hostname, port, query)
        expected_status_code = kwargs.pop('expected_status_code', 200)
        raise_on_status = kwargs.pop('raise_on_status', True)

        resp = requests.get(url, **kwargs)
        if resp.status_code == 404:
            raise IOError
        elif resp.status_code != expected_status_code:
            if raise_on_status:
                raise RuntimeError(resp.status_code)
            else:
                raise IOError

        return load_method(resp.content)
