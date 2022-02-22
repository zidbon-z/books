from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from .models import Book, Shelf
import requests
import json

# Create your views here.
class Index(View):

    def get(self, request):


        context = {
        }

        return render(request, 'main/index.html', context)

    def post(self, request):

        if 'titlebtn' in request.POST:
            searched = request.POST['titleSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + searched, params=request.GET)
            print(r.text)
            stuff = json.loads(r.text)

            context = {
                    'stuff': stuff,
            }

            return render(request, 'main/index.html', context)

        elif 'authorbtn' in request.POST:
            searched = request.POST['authorSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=inauthor:' + searched, params=request.GET)
            print(r.text)
            stuff = json.loads(r.text)

            context = {
                    'stuff': stuff,
            }

            return render(request, 'main/index.html', context)


class Search(View):

    def get(self, request):


        context = {
        }

        return render(request, 'main/search.html', context)

    def post(self, request):

        if 'titlebtn' in request.POST:
            searched = request.POST['titleSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + searched, params=request.GET)
            print(r.text)
            stuff = json.loads(r.text)
            books = list(Book.objects.all().values_list('title', flat=True))

            context = {
                    'stuff': stuff,
                    'books': books,
            }

            return render(request, 'main/search.html', context)

        elif 'authorbtn' in request.POST:
            searched = request.POST['authorSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=inauthor:' + searched, params=request.GET)
            print(r.text)
            stuff = json.loads(r.text)
            books = list(Book.objects.all().values_list('title', flat=True))

            context = {
                    'stuff': stuff,
                    'books': books,
            }

            return render(request, 'main/search.html', context)

        elif 'googleidbtn' in request.POST:
            searched = request.POST['googleidSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes/' + searched, params=request.GET)
            print(r.text)
            stuffs = json.loads(r.text)
            books = list(Book.objects.all().values_list('title', flat=True))

            context = {
                    'stuffs': stuffs,
                    'books': books,
            }

            return render(request, 'main/search.html', context)

class Library(View):

    def get(self, request):

        cur_user = request.user
        library = Book.objects.filter(owner=cur_user)


        return render(request, 'main/library.html', {'library': library,})

def add_book_view(request, googleid):
    searched = googleid
    if request.method == "GET":
        r = requests.get('https://www.googleapis.com/books/v1/volumes/' + searched, params=request.GET)
        print(r.text)
        stuffs = json.loads(r.text)
        print(stuffs)

        title = stuffs["volumeInfo"]["title"]
        authors = stuffs["volumeInfo"]["authors"]
        googleid = stuffs["id"]
        image_link = stuffs["volumeInfo"]["imageLinks"]["thumbnail"]
        new_book = Book(
                        owner = request.user,
                        title = title,
                        authors = authors,
                        googleid = googleid,
                        image_link = image_link,
                        )
        new_book.save()
        next = request.GET.get('next')
        return redirect('main:library')


def add_another_book_view(request):
    searched = request.POST['poop']
    if request.method == "POST":
        r = requests.get('https://www.googleapis.com/books/v1/volumes/' + searched, params=request.GET)
        print(r.text)
        stuffs = json.loads(r.text)
        print(stuffs)

        title = stuffs["volumeInfo"]["title"]
        authors = stuffs["volumeInfo"]["authors"]
        googleid = stuffs["id"]
        image_link = stuffs["volumeInfo"]["imageLinks"]["thumbnail"]
        new_book = Book(
                        owner = request.user,
                        title = title,
                        authors = authors,
                        googleid = googleid,
                        image_link = image_link,
                        )
        new_book.save()

        return HttpResponse('Yo')


