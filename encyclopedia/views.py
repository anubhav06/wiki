from django.core.files.base import ContentFile
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
import random
import markdown2

from . import util


def index(request):
    #If nothing is searched (No request is made)
    if request.POST.get("title") is not None:
        return newPage(request)
    elif request.GET.get("q") is None:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    #If something is searched (A request is made)
    else:
        return search(request)

def title(request, title):
    #For search box 
    if not request.GET.get("q") is None:
        return search(request)

    #For updating entry
    if request.POST.get("title"):
        util.save_entry(title, request.POST.get("content"))

    #Main function
    if util.get_entry(title) is None:  
        return HttpResponseNotFound("ERROR: Requested page was not found") #If no entry exists, head to error page
    else:
        return render(request, "encyclopedia/wiki.html", { #If entry exists, show that entry
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
        })

def search(request): 
    #If something is searched (A request is made)
    title = request.GET.get("q")

    #If exact same word exists
    if util.get_entry(title):                
        return render(request, "encyclopedia/wiki.html", { 
            "title": title,
            "content": markdown2.markdown(util.get_entry(title))
        })
        
    #If exact same word does not exist
    else:
        entries = util.list_entries()
        list=[]
        for entry in entries:
            if title.lower() in entry.lower():
                list.append(entry)
                    
        return render(request, "encyclopedia/search.html", {
            "entries" : list
        })

def newPage(request):
    # For searching
    if request.GET.get("q"):
        return search(request)
    
    if request.POST.get("title") is None:
        return render(request, "encyclopedia/newPage.html")
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")

        entries = util.list_entries()
        for entry in entries:
            if title.lower() in entry.lower():
                return HttpResponseNotFound("ERROR: Title already exists")

        util.save_entry(title, content)
        return redirect("wiki:title", title=title) 


def editPage(request ,title):

    # For searching
    if request.GET.get("q"):
        return search(request)

    if util.get_entry(title) is None:
        return HttpResponseNotFound("ERROR: Requested page was not found")
    else:
        return render(request, "encyclopedia/editPage.html",{
            "title": title,
            "content": util.get_entry(title)
        })

def randomPage(request):
    # For searching
    if request.GET.get("q"):
        return search(request)

    entries = util.list_entries()
    rand = random.choice(entries)
    return redirect("wiki:title", title=rand)