import json

from logstash.formatter import LogstashFormatterVersion1


class LogstashFormatter(LogstashFormatterVersion1):
    """Though the logstash library does most of what we want, it assumes
    the logs are serialized to UDP or TCP, and so converts them to bytes. We
    need them to be strings instead."""
    def serialize(self, message):
        return json.dumps(message)
