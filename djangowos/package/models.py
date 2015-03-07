import bz2
import json

from django.db import models
from django.db.models.signals import post_delete, post_save

class CompressedJSONField(models.BinaryField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', {})
        super(CompressedJSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(CompressedJSONField, self).to_python(value)
        if isinstance(value, buffer):
            value = str(value)
        if isinstance(value, basestring):
            return json.loads(bz2.decompress(value))
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        value = bz2.compress(json.dumps(value))
        return super(CompressedJSONField, self).get_db_prep_value(value, connection, prepared)

class Sync(models.Model):
    """
    Singleton object. Stores the PyPI changelog serial number - this is used
    when requesting incremental updates.
    """

    serial = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.pk = 1
        return super(Sync, self).save(*args, **kwargs)

class Package(models.Model):
    """
    A package's metadata. Represents all packages on PyPI.
    """

    name = models.CharField(max_length=128, unique=True)
    data = CompressedJSONField()

class DjangoPackage(models.Model):
    """
    A Django package. This will be displayed on the site.

    The `active` and `python3` fields are normally copies of the respective
    `pypi_XXX` field, though can be overridden with the `override_XXX` field.
    
    Once created, a DjangoPackage is never deleted, but is instead set to
    inactive. This ensures we don't lose our override settings, and is also why
    we don't have a foreign key to the package model.
    """

    name = models.CharField(max_length=128, unique=True)
    pypi_active = models.BooleanField(default=True)
    pypi_downloads_per_month = models.PositiveIntegerField(db_index=True)
    pypi_python3 = models.NullBooleanField()

    override_active = models.NullBooleanField()
    override_python3 = models.NullBooleanField()
    notes_html = models.CharField(blank=True, max_length=255)

    active = models.BooleanField(default=True, db_index=True)
    python3 = models.NullBooleanField()

    def save(self, *args, **kwargs):
        for attr in ('active', 'python3'):
            override = getattr(self, 'override_{}'.format(attr))
            if override is not None:
                value = override
            else:
                value = getattr(self, 'pypi_{}'.format(attr))
            setattr(self, attr, value)
        return super(DjangoPackage, self).save(*args, **kwargs)

    @classmethod
    def did_save_package(cls, instance, **kwargs):
        if 'django' in json.dumps(instance.data).lower():
            python2 = False
            python3 = None
            for classifier in instance.data['info']['classifiers']:
                if classifier.startswith("Programming Language :: Python :: 2"):
                    python2 = True
                elif classifier.startswith("Programming Language :: Python :: 3"):
                    python3 =  True

            if python2 and not python3:
                python3 = False

            downloads_per_month = instance.data['info']['downloads']['last_month']

            cls.objects.update_or_create(
                name=instance.name,
                defaults=dict(
                    pypi_active=True,
                    pypi_downloads_per_month=downloads_per_month,
                    pypi_python3=python3
                )
            )
        else:
            cls.objects\
                .filter(name=instance.name)\
                .update(active=False)

    @classmethod
    def did_delete_package(cls, instance, **kwargs):
        cls.objects\
            .filter(name=instance.name)\
            .update(active=False)

post_save.connect(DjangoPackage.did_save_package, sender=Package)
post_delete.connect(DjangoPackage.did_delete_package, sender=Package)
