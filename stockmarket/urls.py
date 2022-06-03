from django.conf.urls import url
from . import views

app_name = 'stockmarket'


urlpatterns = [
    # /stockmarket/
    url(r'^$', views.index, name='index'),

    # /stockmarket/login_user/
    url(r'^login_user/$', views.login_user, name='login_user'),

    # /stockmarket/logout_user/
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    # /stockmarket/register
    url(r'^register/$', views.register, name='register'),

    # /stockmarket/mine
    url(r'^mine/$', views.mine, name='mine'),

    # /stockmarket/refresh_database
    url(r'^refresh_database/$', views.refresh_databse, name='refresh_databse'),

    # /stockmarket/<id>/
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),

    # /stockmarket/<id>/favorite/
    url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name="favorite"),

    # /stockmarket/<id>/sell_stock/
    url(r'^(?P<album_id>[0-9]+)/sell_stock/$', views.sell_stock, name="sell_stock"),

    # /stockmarket/<id>/buy_stock/
    url(r'^(?P<album_id>[0-9]+)/buy_stock/$', views.buy_stock, name="buy_stock"),

    # /stockmarket/add/
    url(r'add/$', views.CreateStock.as_view(), name='add'),

    # /stockmarket/search/
    url(r'search/$', views.search, name='search'),

]
