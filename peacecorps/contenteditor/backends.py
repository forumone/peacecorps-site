from django.contrib.auth import backends
from .models import Editor


class EditorBackend(backends.ModelBackend):
    """Always return an Editor rather than a generic User"""

    def get_user(self, user_id):
        try:
            return Editor.objects.get(pk=user_id)
        except Editor.DoesNotExist:
            return None
