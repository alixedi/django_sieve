# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.db.models.loading import get_model
from django.contrib.auth.models import Group
from django.db.models import ManyToManyField


class SieveManager(models.Manager):
    """Use this ModelManager for any models that you want to sieve."""

    def get_related_chain(self, src, tgt):
        """Give a source and a target model, follow relations to get the
        accessor string going from source to target."""
        for f in src._meta.fields + src._meta.many_to_many:
            if f.rel:
                # we are there!
                if f.rel.to == tgt:
                    return f.name
                # tree models! self reference! avoid!
                if f.rel.to == src:
                    continue
                # neither there nor stuck in a tree! keep going!
                re = self.get_related_chain(f.rel.to, tgt)
                # nothing remains downstairs! finish up!
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
        for f in sieve_model._meta.fields + sieve_model._meta.many_to_many:
            if f.rel:
                if not f.rel.to == Group:
                    res.append(f)
        return res

    def get_pivot_objs(self, sieve_qs, pivot_field):
        """Returns all pivot_objs from sieve_qs"""
        res = []
        for obj in sieve_qs:
            val = getattr(obj, pivot_field.name)
            # deal with ManyToMany Fields
            if isinstance(pivot_field, ManyToManyField):
                res = res + list(val.all())
            else:
                res.append(val)
        return res

    def sieve(self, user):
        """Returns queryset filtered according to sieve."""
        sieve_model = self.get_sieve_model()
        model = self.model
        q = models.Q()
        for group in user.groups.all():
            kwargs = {}
            for pivot_field in self.get_pivot_fields(sieve_model):
                pivot_model = pivot_field.rel.to
                sieve_qs = sieve_model.objects.filter(group=group)
                if model == pivot_model:
                    objs = self.get_pivot_objs(sieve_qs, pivot_field)
                    kwargs['pk__in'] = [obj.pk for obj in objs]
                accessor = self.get_related_chain(model, pivot_model)
                if not accessor is None:
                    kwargs[accessor + '__in'] = self.get_pivot_objs(sieve_qs, pivot_field)

            q |= models.Q(**kwargs)
        if q.children == []:
            return self.model.objects.none()
        return self.model.objects.filter(q)

