from django.shortcuts import render


def list(request):
    context = {}
    return render(request, "issues/list.html", context)
