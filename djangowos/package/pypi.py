import json

from pypi_data import AbstractData

from djangowos.package.models import Package, Sync

class Data(AbstractData):
    def _metadata_exists(self, package):
        return Package.object.filter(name=package).exists()

    def _get_metadata(self, package):
        return Package.object.get(name=package).data

    def _set_metadata(self, package, data):
        try:
            Package.objects.update_or_create(name=package, defaults={'data': data})
        except Exception:
            raise

    def _remove_metadata(self, package):
        try:
            Package.objects.filter(name=package).delete()
        except Package.DoesNotExist:
            pass

    def _get_serial(self):
        return Sync.objects.get().serial

    def _set_serial(self, serial):
        Sync.objects.update_or_create(pk=1, defaults={'serial': serial})
