from peacecorps.models import Project

Project.objects.filter(account__code__startswith='15').update(published=True)