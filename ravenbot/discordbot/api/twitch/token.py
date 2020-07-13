from datetime import datetime, timedelta
import logging
from urllib import parse

from ...api import base
from .... import config

LOG = logging.getLogger(__name__)


class TokenSession(base.APIClient):

    def __init__(self, loop):
        super().__init__(loop=loop)
        self._token = None
        self._expires_at = None

    async def get_token(self):
        now = datetime.utcnow()
        need_refresh = True if not self._expires_at else now > self._expires_at

        if need_refresh:
            params = {
                'client_id': config['twitch']['client_id'],
                'client_secret': config['twitch']['client_secret'],
                'grant_type': "client_credentials"
            }
            url = f"https://id.twitch.tv/oauth2/token?{parse.urlencode(params)}"
            token_data = await self.post(url, return_json=True)
            self._token = token_data['access_token']
            self._expires_at = now + timedelta(seconds=token_data['expires_in'])
            LOG.debug(f"New token issued: {token_data['access_token']} (expires on {self._expires_at})")

        return self._token

    async def get_authorization_headers(self):
        token = await self.get_token()
        return {
            'Client-ID': config['twitch']['client_id'],
            'Authorization': f"Bearer {token}"
        }
