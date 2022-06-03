from .models import Stock, Associate, Account, StocksOwned, Transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

from .scrapper import scrap_page, history
import datetime

from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.generic.edit import CreateView


class CreateStock(CreateView):
    model = Stock
    fields = ['symbol', 'countrycode', 'name']


def index(request):
    albums = Stock.objects.all()
    if request.user.is_authenticated:
        associated = Associate.objects.filter(user=request.user)
        stock_liked_list = [associate.stock for associate in associated]

        for album in albums:
            if album in stock_liked_list:
                album.is_favorite = True

    context = {
        "albums": albums,

    }
    return render(request, "stockmarket/index.html", context)


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if len(searched) == 0:
            return render(request, "stockmarket/search.html")
        albums = Stock.objects.filter(name__contains=searched)

        context = {
            "albums": albums,
            "no_alb": len(albums)

        }
        return render(request, "stockmarket/search.html", context)

    else:
        return render(request, "stockmarket/search.html")


@login_required
def mine(request):
    associated = Associate.objects.filter(user=request.user)
    albums = [a.stock for a in associated]
    for stock in albums:
        stock.is_favorite = True

    account = get_object_or_404(Account, user=request.user)
    user_stocks = StocksOwned.objects.filter(owner=request.user)
    user_stocks_owned = 0
    price_total = 0
    cost_per_units = 0
    stocks_types_total = user_stocks.count()

    for user_stock in user_stocks:
        user_stocks_owned += user_stock.amount
        this_stocks_total_price = user_stock.amount * user_stock.stock.price
        price_total += this_stocks_total_price
        cost_per_units += this_stocks_total_price / user_stock.amount
        user_stock.total = this_stocks_total_price
        if user_stock.stock in albums:
            user_stock.stock.is_favorite = True



    if stocks_types_total != 0:
        cost_per_units = cost_per_units / stocks_types_total
        cost_per_units = "{:.2f}".format(cost_per_units)

    alltransactions = Transaction.objects.filter(user=request.user)
    alltransactions = alltransactions.order_by('date')

    recenttransactions = alltransactions
    alltransactions = alltransactions[::-1]

    if recenttransactions.count() > 1:
        transactions_sorted = recenttransactions[::-1]
        recenttransactions = transactions_sorted[:3]

    context = {
        "albums": albums,
        "account": account,
        "user_stocks": user_stocks,
        "no_stocks_owned": user_stocks_owned,
        "price_total": price_total,
        "cost_per_units": cost_per_units,
        "recenttransactions": recenttransactions,
        "alltransactions": alltransactions
    }

    return render(request, "stockmarket/mine.html", context)


# @user_passes_test(lambda u: not u.is_authenticated)
def detail(request, album_id):
    album = get_object_or_404(Stock, pk=album_id)
    old_album = album
    try:
        info = scrap_page(album.symbol, album.countrycode)
        album.price = info["price"]
        album.point_q = info["point_q"]
        album.day_lowest = info["day_lowest"]
        album.day_highest = info["day_highest"]
        album.p_e = info["p_e"]
        album.market_cap = info["market_cap"]
        album.public_float = info["public_float"]
        album.eps = info["eps"]
        album.dividend = info["dividend"]
        if old_album != album:
            album.save()
        graph = history(album.symbol, album.countrycode)
        code = 200
    except:
        print("couldn't recieve data")
        code = "Could not refresh data"
        graph = None

    try:
        Associate.objects.get(user=request.user, stock=album)
        album.is_favorite = True
    except:
        album.is_favorite = False


    try:
        owned = StocksOwned.objects.get(owner=request.user, stock=album)
        owned_stocks = owned.amount
    except:
        owned_stocks = 0

    context = {
        "album": album,
        "code": code,
        "graph": graph,
        "owned_stocks": owned_stocks
    }



    return render(request, "stockmarket/detail.html", context)


@user_passes_test(lambda u: u.is_superuser)
def refresh_databse(request):
    albums = Stock.objects.all()
    bad_stocks = []
    for album in albums:
        try:
            info = scrap_page(album.symbol, album.countrycode)
        except:
            print(f"{album} couldn't be refreshed.")
            bad_stocks.append(album.name)
            continue

        album.price = info["price"]
        album.point_q = info["point_q"]
        album.day_lowest = info["day_lowest"]
        album.day_highest = info["day_highest"]
        album.p_e = info["p_e"]
        album.market_cap = info["market_cap"]
        album.public_float = info["public_float"]
        album.eps = info["eps"]
        album.dividend = info["dividend"]
        album.save()
        print(f"{album} refreshed successfully.")
    print("bad stocks:", bad_stocks)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def sell_stock(request, album_id):
    if request.method == "POST":
        numberofstocks = request.POST['stocks_number']
        numberofstocks = int(numberofstocks)
        album = get_object_or_404(Stock, pk=album_id)

        amount = numberofstocks * album.price

        owned = StocksOwned.objects.get(owner=request.user, stock=album)

        if owned.amount < numberofstocks:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        owned.amount -= numberofstocks


        if owned.amount == 0:
            owned.delete()
        else:
            owned.save()

        account = Account.objects.get(user = request.user)
        account.balance += amount
        account.save()

        transaction = Transaction(user=request.user, stock=album, numberofstocks=numberofstocks, amount=amount, transactiontype="sell", date=datetime.datetime.now())
        transaction.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def buy_stock(request, album_id):
    if request.method == "POST":
        numberofstocks = request.POST['stocks_number']
        numberofstocks = int(numberofstocks)
        album = get_object_or_404(Stock, pk=album_id)

        amount = numberofstocks * album.price
        try:
            owned = StocksOwned.objects.get(owner=request.user, stock=album)
            owned.amount += numberofstocks
            owned.save()
        except:
            owned = StocksOwned(owner=request.user, stock=album, amount=numberofstocks)
            owned.save()

        account = Account.objects.get(user = request.user)
        account.balance -= amount
        account.save()

        transaction = Transaction(user=request.user, stock=album, numberofstocks=numberofstocks, amount=amount,
                                  transactiontype="buy", date=datetime.datetime.now())
        transaction.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))


    else:
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def favorite(request, album_id):
    selected_album = get_object_or_404(Stock, pk=album_id)
    try:
        selected_associate = Associate.objects.get(
            stock=selected_album, user=request.user)
    except(KeyError, Associate.DoesNotExist):
        new_table = Associate(user=request.user, stock=selected_album)
        new_table.save()
    else:
        selected_associate.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'stockmarket/login.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return index(request)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Album.objects.filter(user=request.user)
                return index(request)
            else:
                return render(request, 'stockmarket/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'stockmarket/login.html', {'error_message': 'Invalid login or password!'})
    return render(request, 'stockmarket/login.html')


def register(request):
    if request.user.is_authenticated:
        return index(request)
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                user_account = Account(user=user)
                user_account.save()
                login(request, user)
                return index(request)
    context = {
        "form": form,
    }
    return render(request, 'stockmarket/register.html', context)
