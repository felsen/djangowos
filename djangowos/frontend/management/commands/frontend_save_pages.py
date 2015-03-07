from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        import os
        import os.path

        from django.conf import settings
        from django.test import Client

        URLS = (
            '/',
        )

        client = Client()
        for url in URLS:
            print url
            filename = os.path.join(settings.SITE_ROOT, url.strip('/'), 'index.html')
            path = os.path.dirname(filename)
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise
            response = client.get(url)
            with open(filename, 'w') as fp:
                fp.write(response.content)
