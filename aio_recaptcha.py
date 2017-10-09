from aiohttp import ClientSession
from yarl import URL


class Recaptcha:
    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

    def __init__(self, secret_key):
        self._secret_key = secret_key

    async def verify(self, request):
        params = await request.post()

        peername = request.transport.get_extra_info('peername')
        remote_ip = None
        if peername is not None:
            remote_ip, _ = peername

        url = URL(self.VERIFY_URL).with_query(
            secret=self._secret_key,
            response=params.get('g-recaptcha-response'),
            remoteip=remote_ip,                
        )

        async with ClientSession() as session:
            resp = await session.get(url)
            resp = await resp.json()

        return resp['success']
