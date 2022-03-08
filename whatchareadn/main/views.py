from django.shortcuts import render, redirect

from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .models import Book, Shelf
import requests
import json

############################
# Home page view 
class Index(View):

    def get(self, request):
        r = requests.get('https://www.googleapis.com/books/v1/volumes/h4hHEAAAQBAJ', params=request.GET)
        stuffs = json.loads(r.text)

        isbns = stuffs["volumeInfo"]["industryIdentifiers"]
        for i in isbns:
            a = i['type']
            b = i['identifier']
            if a == 'ISBN_13':
                isbn13 = b
        for i in isbns:
            a = i['type']
            b = i['identifier']
            if a == 'ISBN_10':
                isbn10 = b
        print(isbn10)
        print(isbn13)


        context = {
        }

        return render(request, 'main/index.html', context)


############################
# Search page view 
class Search(View):

    def get(self, request):
        context = {
        }
        return render(request, 'main/search.html', context)

    def post(self, request):

        if 'titlebtn' in request.POST:
            searched = request.POST['titleSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + searched + '&maxResults=40', params=request.GET)
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


############################
# Library page view 
class Library(View):

    def get(self, request):

        cur_user = request.user
        library = Book.objects.filter(owner=cur_user)
        shelves = Shelf.objects.all()


        return render(request, 'main/library.html', {'library': library,
                                                      'shelves': shelves,
                                                     })



def add_book_view(request):
    searched = request.POST['addid']
    if request.method == "POST":
        r = requests.get('https://www.googleapis.com/books/v1/volumes/' + searched, params=request.GET)
        print(r.text)
        stuffs = json.loads(r.text)
        print(stuffs)

        try:
            shelf = Shelf.objects.get(owner=request.user, name="Not on Shelf")
        except:
            new_shelf = Shelf(
                              owner = request.user,
                              name = "Not on Shelf",
                             )
            new_shelf.save()
            shelf = Shelf.objects.get(owner=request.user, name="Not on Shelf")


        title = stuffs["volumeInfo"]["title"]
        selflink = stuffs["selfLink"]
        authorlist = stuffs["volumeInfo"]["authors"]
        for author in authorlist:
            authors = ""
            authors += author
        if "description" in stuffs["volumeInfo"]:
            description = stuffs["volumeInfo"]["description"]
        else:
            description = "description"
        googleid = stuffs["id"]
        image_link = stuffs["volumeInfo"]["imageLinks"]["thumbnail"]
        if "industryIdentifiers" in stuffs["volumeInfo"]:
            isbns = stuffs["volumeInfo"]["industryIdentifiers"]
            for i in isbns:
                a = i['type']
                b = i['identifier']
                if a == 'ISBN_13':
                    isbn13a = b
            for i in isbns:
                a = i['type']
                b = i['identifier']
                if a == 'ISBN_10':
                    isbn10a = b
            if isbn13a:
                isbn13 = isbn13a
            else:
                isbn13 = "no ISBN13"
            if isbn10a:
                isbn10 = isbn10a
            else:
                isbn10 = "no ISBN10"
        else:
            isbn13 = "no ISBN13"
            isbn10 = "no ISBN10"

        new_book = Book(
                        owner = request.user,
                        selflink = selflink,
                        title = title,
                        authors = authors,
                        isbn10 = isbn10,
                        isbn13 = isbn13,
                        description = description,
                        googleid = googleid,
                        image_link = image_link,
                        shelf = shelf,
                        )
        new_book.save()

        return HttpResponse('Yo')

# Delete a book from the Book database table
def delete_book_view(request):
    buttid = request.POST['buttid']
    if request.method == "POST":
        Book.objects.filter(googleid=buttid).delete()
        return HttpResponse('Yo')

############################
# Test page view 
def testpage_view(request):
        cur_user = request.user
        library = Book.objects.filter(owner=cur_user)
        shelves = Shelf.objects.all()
        return render(request, 'main/testpage.html', {'library': library,
                                                      'shelves': shelves,
                                                    })

# Change the shelf for a book
def change_shelf(request):
    cur_user = request.user
    shelfn = request.POST['shelfn']
    bookid = request.POST['bookid']
    if request.method == "POST":
        obj = Book.objects.get(googleid=bookid)
        shelf = Shelf.objects.get(name=shelfn)
        obj.shelf = shelf
        obj.save()
        return HttpResponse('Yo')

#works
def get_shelf(request):
    cur_user = request.user
    shelfname = request.POST['shelf']
    if request.method == "POST":
        if shelfname == "All":
            bookshelf = Book.objects.filter(owner=cur_user)
            shelflist = Shelf.objects.filter(owner=cur_user)
            return JsonResponse({'books': list(bookshelf.values()), 'shelves': list(shelflist.values())})
        else:
            nameshelf = Shelf.objects.get(name=shelfname)
            bookshelf = Book.objects.filter(owner=cur_user, shelf=nameshelf)
            shelflist = Shelf.objects.filter(owner=cur_user)
            return JsonResponse({'books': list(bookshelf.values()), 'shelves': list(shelflist.values())})


def get_book_detail(request):
    searched = request.POST['btnid']
    if request.method == "POST":
        r = requests.get('https://www.googleapis.com/books/v1/volumes/' + searched, params=request.GET)
        print(r.text)
        bookdetail = json.loads(r.text)
        print(bookdetail)

        title = bookdetail["volumeInfo"]["title"]
        if "publisher" in bookdetail["volumeInfo"]:
            publisher = bookdetail["volumeInfo"]["publisher"]
        else:
            publisher = "Not found"
        if "publishedDate" in bookdetail["volumeInfo"]:
            pubdate = bookdetail["volumeInfo"]["publishedDate"]
        else:
            pubdate = "Not found"
        selflink = bookdetail["selfLink"]
        authorlist = bookdetail["volumeInfo"]["authors"]
        for author in authorlist:
            authors = ""
            authors += author
        if "description" in bookdetail["volumeInfo"]:
            description = bookdetail["volumeInfo"]["description"]
        else:
            description = "description"
        googleid = bookdetail["id"]
        image_link = bookdetail["volumeInfo"]["imageLinks"]["thumbnail"]
        if "industryIdentifiers" in bookdetail["volumeInfo"]:
            isbns = bookdetail["volumeInfo"]["industryIdentifiers"]
            for i in isbns:
                a = i['type']
                b = i['identifier']
                if a == 'ISBN_13':
                    isbn13a = b
            for i in isbns:
                a = i['type']
                b = i['identifier']
                if a == 'ISBN_10':
                    isbn10a = b
            if isbn13a:
                isbn13 = isbn13a
            else:
                isbn13 = "no ISBN13"
            if isbn10a:
                isbn10 = isbn10a
            else:
                isbn10 = "no ISBN10"
        else:
            isbn13 = "no ISBN13"
            isbn10 = "no ISBN10"

        response = {
                'title': title,
                'publisher': publisher,
                'pubdate': pubdate,
                'authors': authors,
                'image_link': image_link,
                'description': description,
                'isbn10': isbn10,
                'isbn13': isbn13,
        }
        return JsonResponse(response)






