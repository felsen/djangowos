from django.contrib import admin

from djangowos.package.models import Package, Sync, DjangoPackage

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SyncAdmin(admin.ModelAdmin):
    list_display = ('serial',)

class DjangoPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'pypi_downloads_per_month', 'python3',)
    readonly_fields = ('name', 'active', 'python3', 'pypi_active', 'pypi_downloads_per_month', 'pypi_python3',)
    search_fields = ('name',)

admin.site.register(Package, PackageAdmin)
admin.site.register(Sync, SyncAdmin)
admin.site.register(DjangoPackage, DjangoPackageAdmin)
