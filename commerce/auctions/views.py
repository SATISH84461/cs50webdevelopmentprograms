from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime


from .models import User, auction_listing, categories, watchlist, pro_bid, comments


class create_listing(forms.Form):
    f1 = list((a.cat_name,a.cat_name) for a in categories.objects.all())
    pro_name = forms.CharField(label="Product Name", max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'id':'pro_deatils','placeholder':'Product Name'}))
    pro_description = forms.CharField(label="Product Description", widget=forms.Textarea(attrs={'class':'form-control', 'id':'comment', 'row':'2','placeholder':'Product Description'}))
    pro_price = forms.IntegerField(label="Product Price", widget=forms.TextInput(attrs={'class':'form-control', 'id':'pro_deatils','placeholder':'Product Price'}))
    pro_image = forms.URLField(label="Product Image URL", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'id':'pro_deatils','placeholder':'Product Image URL'}))
    pro_cat_id = forms.ChoiceField(label="Product Categories", choices  = f1, widget=forms.Select(attrs={'class':'form-control','placeholder':'Product Categories'}))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def index(request):
    allitems = set(auction_listing.objects.all())
    inwatchlist = set(watchlist.objects.filter(owner_name=request.user))
    watchlist_pro = set(i.pro_name for i in inwatchlist)
    auction_list = list(allitems.difference(watchlist_pro))
    def by_date(data):
        return data.date
    auction_list.sort(key=by_date,reverse=True)
    return render(request, "auctions/index.html",{
        'name' : "Active Listing",
        'auction_listing': auction_list,
        'user_name' : request.user,
    })


@login_required(login_url="login")
def create_listings(request):
    if request.method == 'POST':
        data = create_listing(request.POST)
        if data.is_valid():
            pro_name = request.POST['pro_name']
            pro_desc = request.POST['pro_description']
            pro_price = request.POST['pro_price']
            pro_image = request.POST['pro_image']
            pro_date = datetime.now()
            pro_cat = request.POST['pro_cat_id']
            pro_cata = ''
            own_name = request.user
            for i in categories.objects.all():
                if i.cat_name == pro_cat:
                    pro_cata = i
            final = auction_listing(pro_name=pro_name, pro_description=pro_desc, pro_price=pro_price,
                                    pro_image=pro_image, date=pro_date, cat_id=pro_cata, owner_name=own_name)
            final.save()
            pro_name = auction_listing.objects.filter(id=final.id)[0]
            bid_complete = pro_bid(owner_name=request.user, pro_name=pro_name, bid_amount=pro_price)
            bid_complete.save()
            return redirect('index')
    form = create_listing()
    return render(request,"auctions/create_listing.html",{
            'create_listing': form,
        })


@login_required(login_url="login")
def pro_categories(request):
    return render(request, "auctions/categories.html",{
        'data' : list(categories.objects.all())
    })


@login_required(login_url="login")
def pro_categories_product(request, name):
    data = categories.objects.filter(cat_name=name)
    #product_list = list(auction_listing.objects.filter(cat_id=data[0].id))
    allitems = set(auction_listing.objects.filter(cat_id=data[0].id))
    inwatchlist = set(watchlist.objects.filter(owner_name=request.user))
    watchlist_pro = set(i.pro_name for i in inwatchlist)
    product_list = list(allitems.difference(watchlist_pro))
    def by_date(data):
        return data.date
    product_list.sort(key=by_date,reverse=True)
    return render(request, "auctions/index.html",{
        'name' : name,
        'auction_listing' : product_list,
    })

@login_required(login_url="login")
def watchlist1(request):
    name = request.user
    product_id_list = watchlist.objects.filter(owner_name=name)
    product_list = []
    for i in product_id_list:
        product_list.append(auction_listing.objects.filter(pro_name=i.pro_name)[0])
    return render(request, "auctions/watchlist.html",{
        'auction_listing' : product_list,
        'name' : "WatchList",
    })

@login_required(login_url="login")
def my_listing(request):
    name = request.user
    products = reversed(auction_listing.objects.filter(owner_name=name))
    return render(request,'auctions/my_listings.html',{
        'auction_listing' : products,
        'name': "My Listing",
    })


@login_required(login_url="login")
def pro_bids(request,g_id):
    error=''
    bider_name = request.user
    pro_details = auction_listing.objects.get(id=g_id)
    maximum_details = pro_bid.objects.filter(owner_name=bider_name,pro_name=pro_details)
    if len(maximum_details)<1:
        maximum = 0
    else:
        maximum = maximum_details[0].bid_amount
    if request.method == "POST":
        bid_price = request.POST["bid"]
        if int(bid_price)>maximum and pro_details.is_running:
             change_bid = pro_bid.objects.filter(pro_name=pro_details)[0]
             change_bid.bid_amount=bid_price
             change_bid.owner_name=request.user
             change_bid.save()
        else:
            error='The Biding Price Should be greater than '+str(maximum)
    pro_details = auction_listing.objects.filter(id=g_id)[0]
    name = User.objects.filter(id=pro_details.owner_name.id)[0]
    cat = categories.objects.filter(id=pro_details.cat_id.id)[0]
    no_bids = pro_bid.objects.filter(pro_name=pro_details)
    maximum=max(list(i.bid_amount for i in no_bids)+[0])
    ll = list(i.pro_name.id for i in watchlist.objects.filter(owner_name=request.user))
    if (pro_details.id in ll):
        in_watch_list=True
    else:
        in_watch_list=False
    is_admin = False
    if request.user == pro_details.owner_name:
        is_admin = True
    winner=''
    if not pro_details.is_running:
        winner = pro_bid.objects.filter(pro_name=pro_details)[0]
    comment = reversed(comments.objects.filter(pro_details=pro_details))
    return render(request, "auctions/product_page.html",{
            "pro_details" : pro_details,
            "name": name.username,
            "cat" : cat.cat_name,
            "date" : pro_details.date.date(),
            "g_id" : g_id,
            "no_bids" : len(no_bids),
            "max_bid" : maximum,
            'in_watch_list': in_watch_list,
            'error': error,
            'is_admin' : is_admin,
            'winner' : winner,
            'comments' : comment,
        })

def add_watchlist(request, g_id):
    pro_details = auction_listing.objects.filter(id=g_id)
    username = request.user
    add_product = watchlist(owner_name=username,pro_name=pro_details[0])
    add_product.save()
    return redirect('watchlist')

def remove_watchlist(request, g_id):
    pro_details = auction_listing.objects.filter(id=g_id)
    username = request.user
    watchlist.objects.filter(owner_name=username,pro_name=pro_details[0]).delete()
    return redirect('watchlist')


def close_listing(request,g_id):
    pro_details = auction_listing.objects.filter(id=g_id)[0]
    pro_details.is_running = False
    pro_details.save()
    return redirect('index')

def add_comment(request,g_id):
    name = request.user
    pro_details = auction_listing.objects.filter(id=g_id)[0]
    user_comment = request.POST['comment']
    comment = comments(name=name, pro_details=pro_details, comment=user_comment)
    comment.save()
    return redirect('pro_bids',g_id=g_id)