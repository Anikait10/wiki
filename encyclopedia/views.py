from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from markdown2 import Markdown
from . import views
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def wiki(request, title):
    print(title)
    x = util.get_entry(title)
    if x is None:
        return render(request, "encyclopedia/error.html", {
            "notfound": True,
        })
    else:
        print(x)
        return render(request, "encyclopedia/entry.html",{
            "title": title, "info": x,
            })

def search(request):
    if request.method == "POST":
        q = request.POST['q'].lower()
        x = util.get_entry(q)
        if x is None:
            all_string =  util.list_entries()
            # print(all_string)
            l = []
            for word in all_string:
                print('w=',word, q)
                if q in word.lower():
                    l.append(word)
                    print('l=', l,q)
            if len(l) == 0:
                return render(request, "encyclopedia/error.html",{
                "notfound": True
                })
            else:
                return render(request, "encyclopedia/index.html", {
                "entries": l
            })

        else:
            print(x)
            return render(request, "encyclopedia/entry.html",{
                "title": q, "info": x,
                })

def createpage(request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        print(title,content)
        markdowner = Markdown()
        content = markdowner.convert(content)

        if util.get_entry(title) is None:
             util.save_entry(title, content)
             return HttpResponseRedirect('wiki/' + title)
        else:
            return render(request, "encyclopedia/error.html",{
            "exists": True
            })
    else:
        return render(request, "encyclopedia/createpage.html")

def editpage(request):
    if request.method =="GET":
        title = request.GET['title']
        info = util.get_entry(title)
        # print(title,info)

        return render(request,"encyclopedia/editpage.html",{
            "info": info,
            "title": title,
                })
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        # print('hititle', title, content)
        markdowner = Markdown()
        content = markdowner.convert(content)
        util.save_entry(title,content)

        return HttpResponseRedirect(reverse('index'))

def randompage(request):
    entries = util.list_entries()
    #print(entries)
    random_page = random.choice(entries)
    #print(random_page)
    return render(request, "encyclopedia/randompage.html",{
    "random":random_page,
    })
