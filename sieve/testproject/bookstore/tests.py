from django.test.client import Client
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User

from bookstore.models import Publisher, Author, Book

from os.path import abspath, dirname, join
PROJECT_ROOT = abspath(dirname(__file__))


class SieveTest(TestCase):

    def setUp(self):
        call_command('loaddata', join(PROJECT_ROOT, 'fixtures/bookstore.json'))
        self.client = Client()

    def test_books(self):
        """
        Test we get the right books for users in different groups - Here we
        have "programming" and "literature".
        """
        # tech_junkie will only ever get "Introduction to C" book
        user = User.objects.get(username='tech_junkie')
        books = list(Book.objects.sieve(user=user).values_list('title', flat=True))
        self.assertEqual([u'Introduction to C'], books)
        # literature_junkie will only ever get "The Alchemist"
        user = User.objects.get(username='literature_junkie')
        books = list(Book.objects.sieve(user=user).values_list('title', flat=True))
        self.assertEqual([u'The Alchemist'], books)

    def test_authors(self):
        """
        Test that we get access to right authors for users in different groups.
        """
         # tech_junkie will only ever get Lafore
        user = User.objects.get(username='tech_junkie')
        authors = list(Author.objects.sieve(user=user).values_list('last_name', flat=True))
        self.assertEqual([u'Lafore'], authors)
        # literature_junkie will only ever get Coelho
        user = User.objects.get(username='literature_junkie')
        authors = list(Author.objects.sieve(user=user).values_list('last_name', flat=True))
        self.assertEqual([u'Coelho'], authors)

    def test_publishers(self):
        """
        Test that we get access to the right publishers for users in different
        groups.
        """
        # tech_junkie will only ever get Wrox
        user = User.objects.get(username='tech_junkie')
        publishers = list(Publisher.objects.sieve(user=user).values_list('name', flat=True))
        self.assertEqual([u'Wrox'], publishers)
        # _junkie will only ever get Wrox
        user = User.objects.get(username='literature_junkie')
        publishers = list(Publisher.objects.sieve(user=user).values_list('name', flat=True))
        self.assertEqual([u'Penguin'], publishers)

