import sys

from aiohttp import web

from aio_recaptcha import Recaptcha


TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<body>
    <form action="/check" method="POST">
        <p class="g-recaptcha" data-sitekey="{site_key}"></p>
        <p>is verify: {is_verify}</p>
        <button type="submit">check captcha</button>
    </form>
    <script src='//www.google.com/recaptcha/api.js'></script>
</body>
</html>
'''


SITE_KEY, SECRET_KEY = sys.argv[1], sys.argv[2]


async def home(request):
    is_verify = request.query.get('is_verify') == '1'
    return web.Response(
        body=TEMPLATE.format(
            site_key=SITE_KEY,
            is_verify=is_verify,
        ),
        content_type='html',
    )


async def check(request):
    recaptcha = request.app.recaptcha
    is_verify = await recaptcha.verify(request)
    return web.HTTPFound(
        request.app.router['home']
        .url_for()
        .with_query(is_verify=1 if is_verify else 0)
    )


def main():
    app = web.Application()

    app.recaptcha = Recaptcha(SECRET_KEY)

    app.router.add_get('/', home, name='home')
    app.router.add_post('/check', check)
    web.run_app(app)


if __name__ == '__main__':
    main()
