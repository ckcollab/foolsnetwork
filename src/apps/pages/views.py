from django.shortcuts import render


def index(request):
    return render(request, "pages/index.html")


def episodes(request):
    return render(request, "pages/episodes.html")
