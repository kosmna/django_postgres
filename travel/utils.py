# -*- coding: utf-8 -*-
import os
import random
import string

from ipware.ip import get_real_ip
from django.forms.models import model_to_dict
from django.utils.deconstruct import deconstructible


def str_trunc(str, max_length=50):
    if len(str) > max_length:
        return u'{0}...'.format(str[:max_length])
    return str


def generate_uid():
    chars = string.digits + string.letters

    return ''.join(random.choice(chars) for _ in range(10))


def get_user_uid(request):
    user_uid = get_real_ip(request)

    # uncomment to local work
    # if not user_uid:
    # user_uid = get_ip(request)

    if not user_uid:
        user_uid = request.session.get('user_uid', None)
        if not user_uid:
            user_uid = generate_uid()

            request.session['user_uid'] = user_uid
    return user_uid


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        uid = generate_uid()
        filename = '{}.{}'.format(uid, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])


