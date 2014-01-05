from django.conf.urls import patterns, url, include
from django.views.generic import ListView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from bookstore.models import Book
from django.contrib.auth.models import User

class BookView(ListView):
	queryset = Book.objects.sieve(user=User.objects.get(pk=1))

urlpatterns = patterns('',
    # Examples:
    url(r'^$', BookView.as_view(), name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)