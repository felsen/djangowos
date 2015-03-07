from django.template.response import TemplateResponse

from djangowos.package.models import DjangoPackage

def index(request, template='frontend/index.html'):
    packages = DjangoPackage.objects\
        .filter(active=True)\
        .select_related('package')\
        .order_by('-pypi_downloads_per_month')\
        [:200]

    python3 = []
    python2 = []
    for index, package in enumerate(packages):
        package.ranking = index + 1
        if package.python3:
            python3.append(package)
        else:
            python2.append(package)

    python3_percent = float(len(python3)) / (len(python3) + len(python2)) * 100
    python2_percent = float(len(python2)) / (len(python3) + len(python2)) * 100

    return TemplateResponse(request, template, {
        'python3': python3,
        'python2': python2,
        'python3_percent': python3_percent,
        'python2_percent': python2_percent
    })
