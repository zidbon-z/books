from django.shortcuts import render
from django.views import View
import requests
import json

# Create your views here.
class Index(View):

    def get(self, request):

        search = "one piece"
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + search, params=request.GET)
        print(r.text)
        stuff = json.loads(r.text)

        context = {
                'stuff': stuff,
        }

        return render(request, 'main/index.html', context)
