# coding=utf-8
from django import forms
from django.db import models
import phonenumbers
from django.core import validators
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError


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