from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django import forms
from markdown2 import Markdown
from random import choice
from . import util

class CreateNewPageForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(widget=forms.Textarea, label='Content')

def index(request):
    return render(request, "encyclopedia/index1.html")


def wiki(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    entry_content = util.get_entry(entry_name)
    if entry_content:
        entry_content_markdown = Markdown().convert(entry_content)
        return render(request, 'encyclopedia/entry.html', {'entry_name':entry_name, 'entry_content_markdown':entry_content_markdown})
    else:
        raise Http404('Entry not found')

def search(request):
    search_string = request.GET['q']
    if util.get_entry(search_string):
        return redirect('encyclopedia:entry', entry_name=search_string)
    else:
        #get all entries
        entries = util.list_entries()

        #result array
        result = []

        for entry in entries:
            if search_string in entry:
                result.append(entry)

        return render(request, 'encyclopedia/search.html', {'entries':result})

def create_new_page(request):
    if request.method == 'POST':
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title in util.list_entries():
                raise PermissionDenied
            else:
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return redirect('encyclopedia:index')
        else:
            return render(request, 'encyclopedia/create_new_page.html', {'form':form})
    else:
        return render(request, 'encyclopedia/create_new_page.html', {'form':CreateNewPageForm()})

def edit_entry(request):
    if request.method == 'POST':
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', entry_name=title)
        else:
            return render(request, 'encyclopedia/edit_entry.html', {'form':form})
    else:
        entry_name = request.GET['title']
        if entry_name:
            form = CreateNewPageForm({'title':entry_name, 'content':util.get_entry(entry_name)})
            return render(request, 'encyclopedia/edit_entry.html', {'form':form})
        else:
            raise PermissionDenied

def random_entry(request):
    random_entry_name = choice(util.list_entries())
    return redirect('encyclopedia:entry', entry_name=random_entry_name)