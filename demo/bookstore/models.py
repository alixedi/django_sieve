from django.db import models
from sieve.models import SieveManager

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    objects = SieveManager()

    def __unicode__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    objects = SieveManager()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    objects = SieveManager()

    def __unicode__(self):
        return self.title

# the pivot columns may be many-to-many! bit simple first.
class Sieve(models.Model):
    user = models.ForeignKey('auth.User')
    publisher = models.ForeignKey(Publisher)
    author = models.ForeignKey(Author)

    def __unicode__(self):
        return '%s - %s - %s' % (self.user.email, 
                                 self.publisher.name, 
                                 self.author.email)
