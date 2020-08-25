from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new", views.create_new, name="create_new"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path('place_bid/<str:listing_id>', views.place_bid, name="place_bid"),
    path('watchlist', views.watchlist, name='watchlist'),
    path('comment/<str:listing_id>', views.comment, name='comment'),
    path('accept_bid.<str:listing_id>', views.accept_bid, name="accept_bid"),
    # path('filter/<str:category_id>', views.filter, name="filter")
]
