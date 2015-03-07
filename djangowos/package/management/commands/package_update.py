from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """
        Update packages from PyPI.
        """

        from djangowos.package.models import Sync
        from djangowos.package.pypi import Data

        data = Data()
        if Sync.objects.exists():
            data.update()
            # TODO: Update packages not returned above, but have an active
            # DjangoPackage. This will update the download stats.
        else:
            data.init()
