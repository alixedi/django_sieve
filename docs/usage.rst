========
Usage
========

To use django_sieve in a project:

1. Include it in INSTALLED_APPS in your settings file.

2. Define a sieve model. A sieve model is the control for defining the filtering criteria of user data. For instance, in our example, we have a bookstore in which a user can subscribe to all the books from a particular author or all the books from a few publishers. In this case, his book list need to only contain books from the author and publishers that he has chosen. In order to do this, we define a sieve model like so: ::

	class Sieve(models.Model):
		group = models.ForeignKey('auth.Group')
		publisher = models.ManyToManyField(Publisher)
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

That is all. Site-wide filtering of user data based on predefined criteria without having to write queries for all the views. 

Please be wary of performance issues though - in our experience, django-sieve works for 90% cases especially when you need to bring everything up for a quick demo. However, as your site matures and the number of users increase, you may want to invest in profiling your views and hand-crafting these queries when and where required.
