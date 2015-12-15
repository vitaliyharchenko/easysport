# coding=utf-8
from django import forms
from django.db import models
import phonenumbers
from django.core import validators
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError

import urllib
from django.core.files import File


# Beauty image widget for admin
#
#
class BeautyImageWidget(forms.FileInput):
    existing = '<img src="{url}" alt="{name}" width="{width}" height="{height}">'

    html = """\
            <br>
            <div>
                {image}
                <input type="file" name="{name}" accept="images/*"></span>
            </div>
           """

    def __init__(self, attrs={}):
        super(BeautyImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        state = 'exists' if value else 'new'
        width = attrs.get('width', None) or 150
        height = attrs.get('width', None) if value else 150
        existing = self.existing.format(url=value.url, name=name, width=width, height=height) if value else ''
        return self.html.format(state=state, width=width, height=height, image=existing, name=name)


# Jasny image widget
#
#
class JasnyImageWidget(forms.FileInput):
    existing = '<img src="{url}" alt="{name}" width="{width}" height="{height}">'

    html = """\
            <br>
            <div class="fileinput fileinput-{state}" data-provides="fileinput">
                <div class="fileinput-preview thumbnail" style="width: {width}px; height: {height}px;">
                    {image}
                </div>
                <div>
                    <span class="btn btn-default btn-file">
                        <span id="a-jasny-add" class="fileinput-new">Выберите изображение</span>
                        <span class="fileinput-exists">Изменить</span>
                        <input type="file" name="{name}" accept="images/*"></span>
                        <input type="hidden" id="jasny-deleted" name="{name}-deleted" value="0">
                        <input type="hidden" value name>
                    </span>
                    <a href="#" id="a-jasny-deleted" class="btn btn-default fileinput-exists" data-dismiss="fileinput">Удалить</a>
                </div>
            </div>
           """

    def __init__(self, attrs={}):
        super(JasnyImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        state = 'exists' if value else 'new'
        width = attrs.get('width', None) or 150
        height = attrs.get('width', None) if value else 150
        existing = self.existing.format(url=value.url, name=name, width=width, height=height) if value else ''
        return self.html.format(state=state, width=width, height=height, image=existing, name=name)

    # def value_from_datadict(self, data, files, name):
    #     deleted = bool(int(data.pop(name+'-deleted', ['0'])[0]))
    #     url = data.pop(name+'-url', [''])[0]
    #     file = files.get(name, None)
    #     if deleted and not file:
    #         return False
    #     if not file and url:
    #         result = urllib.urlretrieve(url)
    #         file = File(open(result[0]))
    #     return file

    class Media:
        css = {
            'all': ['css/jasny.css']
        }
        js = ['js/jasny.js']


# CUSTOM PHONE FIELD
#
#
def to_standart(value):
    try:
        x = phonenumbers.parse(value, "RU")
        phone_number = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return value
    return phone_number


def validate_russian_phonenumber(value):
    try:
        x = phonenumbers.parse(value, "RU")
    except NumberParseException:
        raise ValidationError('Похоже, что это неправильный номер телефона')


class PhoneNumberDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = to_standart(value)


class PhoneField(models.Field):

    description = "Номер телефона"
    descriptor_class = PhoneNumberDescriptor
    default_validators = [validate_russian_phonenumber]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 128)
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))

    def get_internal_type(self):
        return 'CharField'

    def contribute_to_class(self, cls, name):
        super(PhoneField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
        }
        defaults.update(kwargs)
        return super(PhoneField, self).formfield(**defaults)