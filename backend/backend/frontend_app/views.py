from django.shortcuts import render


def front(request):
    context = {}
    return render(request, "index.html", context)


def catch_all(request, path):
    context = {}
    return render(request, "index.html", context)
