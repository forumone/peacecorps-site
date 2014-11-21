import json

from django.contrib.auth import backends
from logstash.formatter import LogstashFormatterVersion1

from .models import Editor


class EditorBackend(backends.ModelBackend):
    """Always return an Editor rather than a generic User"""

    def get_user(self, user_id):
        try:
            return Editor.objects.get(pk=user_id)
        except Editor.DoesNotExist:
            return None


class LogstashFormatter(LogstashFormatterVersion1):
    """Though the logstash library does most of what we want, it assumes
    the logs are serialized to UDP or TCP, and so converts them to bytes. We
    need them to be strings instead."""
    def serialize(self, message):
        return json.dumps(message)
