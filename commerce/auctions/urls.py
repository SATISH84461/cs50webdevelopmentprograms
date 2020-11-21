from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing",views.create_listings, name="create_listing"),
    path("categories",views.pro_categories, name="categories"),
    path("my_listing",views.my_listing,name="my_listing"),
    path('add_comments/<int:g_id>',views.add_comment,name='add_comment'),
    path("close_listing/<str:g_id>",views.close_listing,name="close_listing"),
    path("categories/<str:name>",views.pro_categories_product, name="categories_product"),
    path("watchlist",views.watchlist1,name="watchlist"),
    path('watchlist/add/<str:g_id>',views.add_watchlist,name="addwatchlist"),
    path('watchlist/remove/<str:g_id>',views.remove_watchlist,name="removewatchlist"),
    path("<str:g_id>",views.pro_bids,name="pro_bids"),
]
