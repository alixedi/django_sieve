# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.db.models.loading import get_model
from django.contrib.auth.models import User

class SieveManager(models.Manager):
    """Use this ModelManager for any models that you want to sieve."""

    def get_related_chain(self, src, tgt):
        """Give a source and a target model, follow relations to get the
        accessor string going from source to target."""
        for f in src._meta.fields + src._meta.many_to_many:
            if f.rel:
                if f.rel.to == tgt:
                    return f.name
                re = self.get_related_chain(f.rel.to, tgt)
                if not re is None:
                    return '%s__%s' % (f.name, re)

    def get_sieve_model(self):
        """Returns the model class for the model name defined as sieve via
        SIEVE_MODEL settings in settings.py"""
        app_label, model_name = getattr(settings, 'SIEVE_MODEL').split('.')
        return get_model(app_label, model_name)

    def get_pivot_fields(self, sieve_model):
        """Returns the pivot fields given sieve model"""
        res = []
        for f in sieve_model._meta.fields:
            if f.rel:
                if not f.rel.to == User:
                    res.append(f)
        return res

    def get_pivot_objs(self, sieve_qs, pivot_field):
        """Returns all pivot_objs from sieve_qs"""
        res = []
        for obj in sieve_qs:
            res.append(getattr(obj, pivot_field.name))
        return res

    def sieve(self, user):
        """Returns queryset filtered according to sieve."""
        sieve_model = self.get_sieve_model()
        model = self.model
        kwargs = {}
        for pivot_field in self.get_pivot_fields(sieve_model):
            pivot_model = pivot_field.rel.to
            accessor = self.get_related_chain(model, pivot_model)
            sieve_qs = sieve_model.objects.filter(user=user)
            kwargs[accessor + '__in'] = self.get_pivot_objs(sieve_qs, pivot_field)
        return self.model.objects.filter(**kwargs)

