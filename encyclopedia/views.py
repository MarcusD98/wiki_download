from django.shortcuts import render, redirect
from . import util
import markdown2
import random
from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {"message": "Page not found."})
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(entry_content)
    })

def search(request):
    query = request.GET.get("q", "")
    if util.get_entry(query) is not None:
        return redirect('entry', title=query)
    else:
        entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {"entries": entries, "query": query})

def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "existing": True
                })
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/create.html", {
        "form": form,
        "existing": False
    })

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)