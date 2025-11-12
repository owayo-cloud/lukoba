from django.urls import path
from . import views

urlpatterns = [
    # Public routes
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('movies/', views.movies_list, name='movies'),
    path('movies/<str:imdb_id>/', views.movie_detail, name='movie_detail'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Booking
    path('movies/<str:imdb_id>/book/', views.booking_page, name='booking'),
    path('movies/<str:imdb_id>/book/submit/', views.book_post, name='book_post'),
    path('movies/<str:imdb_id>/payment/<int:booking_id>/', views.payment_status, name='payment_status'),
    path('movies/<str:imdb_id>/payment_failed/', views.payment_failed, name='payment_failed'),
    
    # M-Pesa callback
    path('mpesa_callback/', views.mpesa_callback, name='mpesa_callback'),
    
    # Admin dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/movies/', views.dashboard_movies, name='dashboard_movies'),
    path('dashboard/movies/<str:imdb_id>/', views.dashboard_movie_detail, name='dashboard_movie_detail'),
    path('dashboard/movies/<str:imdb_id>/add-showtime/', views.add_movie_showtime, name='add_movie_showtime'),
    path('dashboard/movies/showtime/<int:showtime_id>/delete/', views.delete_showtime, name='delete_showtime'),
    path('dashboard/bookings/', views.dashboard_bookings, name='dashboard_bookings'),
    path('dashboard/users/', views.dashboard_users, name='dashboard_users'),
    path('reports/', views.generate_reports, name='reports'),
]
