from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util, forms
import random as rand


def index(request):
    if request.method == "POST":
        entries = util.list_entries()
        query = request.POST['q'].lower()
        if query in list(map(lambda x: x.lower(), entries)):
            return HttpResponseRedirect(reverse("wiki:entry-page", args=[query]))
        else:
            matches = [entry for entry in entries if query in entry.lower()]
            return render(request, "encyclopedia/search.html", {"query": query, "entries": matches})

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    entries = util.list_entries()

    try:
        title = entries[list(map(lambda x: x.lower(), entries)).index(title)]

    finally:
        content = util.get_entry(title)

        if content:
            content = Markdown().convert(content)

        return render(
            request,
            "encyclopedia/entry-page.html",
            {"title": title, "content": content},
        )

def random(request):
    title = rand.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:entry-page", args=[title]))


def add(request):
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data["title"]
            entries = list(map(lambda x: x.lower(), util.list_entries()))
            if title.lower() in entries:
                return render(
                    request,
                    "encyclopedia/add.html",
                    {
                        "form": form,
                        "error": "ERROR: An article with that title already exists.",
                    },
                )
            else:
                util.save_entry(title, data["content"])
                return HttpResponseRedirect(reverse("wiki:entry-page", args=[title]))
        else:
            return render(request, "encyclopedia/add.html", {"form": form})
    else:
        return render(request, "encyclopedia/add.html", {"form": forms.NewEntryForm()})


def edit(request, title):
    if request.method == "POST":
        form = forms.EditEntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            util.save_entry(title, data["content"])
            return HttpResponseRedirect(reverse("wiki:entry-page", args=[title]))
    else:
        content = util.get_entry(title)
        form = forms.EditEntryForm({"content": content})

    return render(request, "encyclopedia/edit.html", {"title": title, "form": form})
