# Thanks blackrobot
# http://djangosnippets.org/snippets/2868/
import csv
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.db.models.fields.files import FieldFile


def prep_field(request, obj, field, manyToManySep=';'):
    """ Returns the field as a unicode string. If the field is a callable, it
    attempts to call it first, without arguments.
    """
    if '__' in field:
        bits = field.split('__')
        field = bits.pop()

        for bit in bits:
            obj = getattr(obj, bit, None)

            if obj is None:
                return ""

    attr = getattr(obj, field)

    if isinstance(attr, (FieldFile,) ):
        attr = request.build_absolute_uri(attr.url)

    output = attr() if callable(attr) else attr

    if isinstance(output, (list, tuple, QuerySet)):
        output = manyToManySep.join([str(item) for item in output])

    return str(output) if output else ""


def export_csv_action(description="Export as CSV",
                      fields=None,
                      exclude=None,
                      header=True,
                      manyToManySep=';'):
    """ This function returns an export csv action. """
    def export_as_csv(modeladmin, request, queryset):
        """ Generic csv export admin action.
        Based on http://djangosnippets.org/snippets/2712/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]
        labels = []

        if exclude:
            field_names = [f for f in field_names if f not in exclude]

        elif fields:
            field_names = [field for field, _ in fields]
            labels = [label for _, label in fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
            str(opts).replace('.', '_')
        )

        writer = csv.writer(response)

        if header:
            writer.writerow(labels if labels else field_names)

        for obj in queryset:
            writer.writerow([prep_field(request, obj, field, manyToManySep) for field in field_names])
        return response
    export_as_csv.short_description = description
    export_as_csv.acts_on_all = True
    return export_as_csv
