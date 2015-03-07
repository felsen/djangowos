from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """
        Save all Package objects. Can be useful when developing.
        """

        from djangowos.package.models import Package

        for package in Package.objects.all():
            print package.name
            package.save()
