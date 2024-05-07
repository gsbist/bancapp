from django.shortcuts import render
from .tasks import read_data


def home(request):

    if request.method == "POST":
        read_data.delay()

    return render(request, "home.html")
