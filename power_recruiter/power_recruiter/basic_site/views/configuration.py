from django.shortcuts import render


def configuration(request):
    context = None
    return render(request, "configuration.html", context)
