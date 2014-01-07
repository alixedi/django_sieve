=============================
django_sieve
=============================

.. image:: https://badge.fury.io/py/django_sieve.png
    :target: http://badge.fury.io/py/django_sieve
    
.. image:: https://travis-ci.org/alixedi/django_sieve.png?branch=master
        :target: https://travis-ci.org/alixedi/django_sieve

.. image:: https://pypip.in/d/django_sieve/badge.png
        :target: https://crate.io/packages/django_sieve?version=latest


Filter user-data based on multiple criteria.

Installation
------------

We are at the cheeseshop: ::

	pip install django_sieve

Usage
-----

To use django_sieve in a project:

1. Include it in INSTALLED_APPS in your settings file.

2. Define a sieve model. A sieve model is the control for defining the filtering criteria for user data. For instance, in our example, we have a bookstore in which a user can subscribe to all the books from a particular author or all the books from a particular publisher. In this case, his book list need to only contain books from the publisher and author that he has chosen. In order to do this, we define a sieve model like so: ::

	class Sieve(models.Model):
		user = models.ForeignKey('auth.User')
		publisher = models.ForeignKey(Publisher)
		author = models.ForeignKey(Author)

3. Declare your project-wide sieve model in `settings.py`. For instance, if the sieve model is called Sieve and resides in the bookstore app: ::

	SIEVE_MODEL = 'bookstore.Sieve'

4. Use `SieveManager` as the ModelManager for all the models in your project that you want to filter based on the criteria defined in the sieve model: ::

	class Author(models.Model):
		first_name = models.CharField(max_length=30)
		last_name = models.CharField(max_length=40)
		email = models.EmailField()
		objects = SieveManager()

5. Use the `sieve` method to define your queryset in your views like so: ::

	class BookView(ListView):
		queryset = Book.objects.sieve(user=request.user)

That is all. Site-wide filtering of user-data based on pre-defined criteria without having to write queries for all the views. Please be wary of performance issues though - in our experience, django-sieve works for 90% cases especially when you need to bring everything up for a quick demo. However, as your site matures and the number of users increase, you may want to invest in profiling your views and hand-crafting these queries when and where required.