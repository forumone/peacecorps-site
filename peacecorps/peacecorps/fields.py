import json
import logging

from django.conf import settings
from django.db import models
import gnupg

from sirtrevor import SirTrevorContent
from sirtrevor.fields import SirTrevorField


class GPGField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, gpg_check=False, *args, **kwargs):
        """gpg_check is used during migrations. It'll warn the user if GPG is
        not set up"""
        if gpg_check and not settings.GNUPG_HOME:
            logging.warning('GNUPG_HOME not set up; will not encrypt/decrypt')
        super(GPGField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        """We use a binary field type to draw a stark distinction between
        encrypted data (binary) and non-encrypted data (strings)"""
        return 'BinaryField'

    def gpg(self):
        """Set up GPG; not taxing, so performed on the fly, making it easier
        to test"""
        if settings.GNUPG_HOME:
            return gnupg.GPG(gnupghome=settings.GNUPG_HOME)

    def to_python(self, value):
        """Convert ciphertext into plaintext"""
        if value is None:
            return value

        if isinstance(value, str):
            return value

        if isinstance(value, memoryview):
            value = value.tobytes()

        gpg = self.gpg()
        if gpg:
            return gpg.decrypt(value).data.decode('utf-8')
        else:   # No GPG; assume the value is plain text
            return value.decode('utf-8')

    def get_prep_value(self, value):
        """Convert plaintext into ciphertext"""
        if value is None:
            return value

        plain_text = value.encode('utf-8')
        field_path = '%s.%s.%s' % (self.model._meta.app_label,
                                   self.model._meta.object_name,
                                   self.name)
        recipient = settings.GPG_RECIPIENTS[field_path]
        gpg = self.gpg()
        if gpg:
            return gpg.encrypt(plain_text, [recipient]).data
        else:   # No GPG; just stick it in the DB
            return plain_text


class BraveSirTrevorContent(SirTrevorContent):
    """Django Sir Trevor is very sensitive about data integrity. Be a tad more
    lenient"""
    @property
    def html(self):
        try:
            return super(BraveSirTrevorContent, self).html
        except ValueError:
            return SirTrevorContent(json.dumps({"data": [
                {"type": "text",
                 "data": {"text": "# ***DATA FORMAT INCORRECT***\n"
                                  + self}}]})).html


class BraveSirTrevorField(SirTrevorField):
    """Extended version of the sir trevor django library"""

    def value_to_string(self, obj):
        sirtrev = self._get_val_from_obj(obj)
        return str(sirtrev)

    def to_python(self, value):
        if value is None:
            value = ""
        return BraveSirTrevorContent(value)
