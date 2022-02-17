from django.shortcuts import render
from django.views import View
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

        search = "one piece"
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + search, params=request.GET)
        print(r.text)
        stuff = json.loads(r.text)

        context = {
                'stuff': stuff,
        }

        return render(request, 'main/search.html', context)

    def post(self, request):

        if 'titlebtn' in request.POST:
            searched = request.POST['titleSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + searched, params=request.GET)
            print(r.text)
            stuff = json.loads(r.text)

            context = {
                    'stuff': stuff,
            }

            return render(request, 'main/search.html', context)

        elif 'authorbtn' in request.POST:
            searched = request.POST['authorSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=inauthor:' + searched, params=request.GET)
            print(r.text)
            stuff = json.loads(r.text)

            context = {
                    'stuff': stuff,
            }

            return render(request, 'main/search.html', context)

        elif 'googleidbtn' in request.POST:
            searched = request.POST['googleidSearch']

            r = requests.get('https://www.googleapis.com/books/v1/volumes/' + searched, params=request.GET)
            print(r.text)
            stuffs = json.loads(r.text)

            context = {
                    'stuffs': stuffs,
            }

            return render(request, 'main/search.html', context)
