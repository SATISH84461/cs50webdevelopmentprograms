from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from markdown2 import Markdown
from random import choice


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'margin':'4%'}))
    description = forms.CharField(label="Description",widget=forms.Textarea)

class editform(forms.Form):
    desc = forms.CharField(label="Description",widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def new_page(request):
    if request.method == "POST":
        form =NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            title = title.capitalize()
            if util.get_entry(title)==None:
                util.save_entry(title,desc)
                return redirect(f"/wiki/{title}")
            else:
                return render(request, 'encyclopedia/page.html',{
                    'name': 'Error',
                    'data': '<h1>Sorry, Page Already Exist'
                })
    else:
        return render(request, "encyclopedia/create_new_page.html",{
            'form':NewTaskForm()
        })

def gget_page(request, name):
    files = util.get_entry(name)
    if(files!=None):
        data = Markdown().convert(f"{files}")
        return render(request, 'encyclopedia/page.html',{
            'name':name,
            'data': data
        })
    else:
        return HttpResponse("<h1>Sorry</h1>")


def edit_page(request,name):
    files=util.get_entry(name)
    if request.method == "POST":
        form = editform(request.POST)
        if form.is_valid():
            desc = form.cleaned_data["desc"]
            util.save_entry(name,desc)
            #return HttpResponse(f"{desc}")
            return redirect(f"/wiki/{name}")
    else:
        if(files):
            return render(request, "encyclopedia/edit_page.html", {'form':editform(initial = {'desc':files}), 'name':name})
        else:
            return HttpResponse("<h1>Sorry</h1>")


def random_page(request):
    title = choice(util.list_entries())
    #files = util.get_entry(title)
    return redirect(f"/wiki/{title}")
    '''return render(request, 'encyclopedia/page.html',{
                    'name': title,
                    'data': Markdown().convert(f"{files}")
                })'''


def search_result(request):
    find = request.GET['q']
    find=find.capitalize()
    data = util.list_entries()
    lis = []
    for i in data:
        if find in i:
            lis.append(i)
    if len(lis)!=0 and find==lis[0]:
        return redirect(f'/wiki/{find}')
    elif len(lis)>0:
        return render(request, 'encyclopedia/search_result.html',{
                    'name': 'Search Result',
                    'lis': lis
                })
    else:
        return render(request, 'encyclopedia/page.html',{
                        'name': 'Error',
                        'data': "<h1>Sorry, Page is not Available</h1>"
                    })