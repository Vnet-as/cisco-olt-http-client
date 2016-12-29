
from cisco_olt_http.client import Client


class TestClientSimple:

    @classmethod
    def setup_class(cls):
        cls.client = Client('http://base-url')

    def test_token_inc(self):
        t = self.client.token
        assert self.client.token == t + 1

    def test_login(self, mocker):
        mocker.patch.object(self.client.session, 'post')
        self.client.session.post.side_effect = mocker.Mock()
        self.client.login('username', 'password')
        self.client.session.post.assert_called_once_with(
            'http://base-url/login.htm',
            data={
                'myusername': 'username',
                'mypassword': 'password',
                'button': 'Login',
                'textfield': 'UX_EQUIPNAME',
            })
