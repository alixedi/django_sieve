from django.conf.urls import patterns, url, include
from django.views.generic import ListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from bookstore.models import Book, Publisher, Author
from django.contrib.auth.models import User

class BookView(ListView):
	queryset = Book.objects.sieve(user=User.objects.get(pk=1))

class AuthorView(ListView):
	queryset = Author.objects.sieve(user=User.objects.get(pk=1))

class PublisherView(ListView):
	queryset = Publisher.objects.sieve(user=User.objects.get(pk=1))


urlpatterns = patterns('',
    # Examples:
    url(r'^books/$', BookView.as_view(), name='books'),
    url(r'^authors/$', AuthorView.as_view(), name='authors'),
    url(r'^publishers/$', PublisherView.as_view(), name='publishers'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)