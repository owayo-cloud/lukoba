import random
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum, Count
from django.db import transaction
from django.conf import settings
from .models import Movie, Showtime, Seat, Booking, Payment, User
from .utils import get_movie_data, search_movies, generate_access_token, lipa_na_mpesa_online

PREDEFINED_TITLES = [
    'Inception', 'The Dark Knight', 'Interstellar', 'The Matrix', 'Pulp Fiction',
    'Fight Club', 'The Shawshank Redemption', 'The Godfather', 'The Avengers', 'The Social Network'
]


def home(request):
    """Home page with movie carousel"""
    movies = Movie.objects.all()[:10]
    return render(request, 'home.html', {'movies': movies})


def contacts(request):
    """Contact page"""
    return render(request, 'contacts.html')


def movies_list(request):
    """Movies listing page with search"""
    title = request.GET.get('title', '')
    movies = []
    
    if title:
        movies = search_movies(title)
    else:
        # Get random query from predefined list
        title = random.choice(PREDEFINED_TITLES)
        movies = search_movies(title)
    
    return render(request, 'movies.html', {'movies': movies})


def movie_detail(request, imdb_id):
    """Movie detail page"""
    movie_data = get_movie_data(imdb_id)
    if not movie_data:
        return render(request, '404.html', status=404)
    
    # Get movie from database
    movie = Movie.objects.filter(imdb=imdb_id).first()
    showtimes = movie.showtimes.all() if movie else None
    
    return render(request, 'movie_detail.html', {
        'movie': movie_data,
        'movie_obj': movie,
        'showtimes': showtimes
    })


@login_required
def booking_page(request, imdb_id):
    """Booking page with seat selection"""
    showtime_id = request.GET.get('s')
    movie = get_object_or_404(Movie, imdb=imdb_id)
    showtimes = movie.showtimes.all()
    
    booked_seats = []
    showtime_obj = None
    
    if showtime_id:
        try:
            showtime_obj = Showtime.objects.get(id=showtime_id, movie=movie)
            booked_seats = list(showtime_obj.seats.filter(is_booked=True).values_list('seat_number', flat=True))
        except Showtime.DoesNotExist:
            pass
    
    # Convert booked_seats to JSON for JavaScript
    booked_seats_json = json.dumps(booked_seats)
    
    return render(request, 'booking.html', {
        'movie': movie,
        'showtimes': showtimes,
        'showtime_obj': showtime_obj,
        'booked_seats': booked_seats_json
    })


@login_required
@require_http_methods(["POST"])
def book_post(request, imdb_id):
    """Handle booking submission"""
    movie_id = request.POST.get('movie')
    seats = request.POST.get('seats', '')
    showtime_id = request.POST.get('showtime')
    phone_number = request.POST.get('phone_number')
    amount = request.POST.get('amount')
    
    try:
        movie = Movie.objects.get(id=movie_id)
        showtime = Showtime.objects.get(id=showtime_id)
    except (Movie.DoesNotExist, Showtime.DoesNotExist):
        return HttpResponse("Movie or showtime not found.", status=400)
    
    # Check if seats are available
    selected_seats = [s.strip() for s in seats.split(',') if s.strip()]
    booked_seats = set(showtime.seats.filter(is_booked=True).values_list('seat_number', flat=True))
    
    if any(seat in booked_seats for seat in selected_seats):
        return HttpResponse("Some selected seats are already booked.", status=400)
    
    # M-Pesa integration
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    business_short_code = settings.MPESA_BUSINESS_SHORT_CODE
    lipa_na_mpesa_online_passkey = settings.MPESA_LIPA_NA_MPESA_ONLINE_PASSKEY
    callback_url = settings.MPESA_CALLBACK_URL
    account_reference = 'LuKoBa'
    transaction_desc = 'Payment for booking'
    
    access_token = generate_access_token(consumer_key, consumer_secret)
    if not access_token:
        return HttpResponse("Failed to generate access token.", status=500)
    
    payment_response = lipa_na_mpesa_online(
        access_token,
        business_short_code,
        lipa_na_mpesa_online_passkey,
        amount,
        phone_number,
        callback_url,
        account_reference,
        transaction_desc
    )
    
    # Check if payment was successful
    if payment_response.get('ResponseCode') == '0':
        with transaction.atomic():
            # Create payment
            payment = Payment.objects.create(
                payment_method='mpesa',
                amount=float(amount),
                transaction_id=phone_number
            )
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                showtime=showtime,
                payment=payment
            )
            
            # Create seats
            for seat_number in selected_seats:
                Seat.objects.create(
                    showtime=showtime,
                    seat_number=seat_number,
                    is_booked=True,
                    booking=booking
                )
            
            # Update available seats
            showtime.seats_available -= len(selected_seats)
            showtime.save()
        
        return redirect('payment_status', imdb_id=imdb_id, booking_id=booking.id)
    else:
        return redirect('payment_failed', imdb_id=imdb_id)


@login_required
def payment_status(request, imdb_id, booking_id):
    """Payment status page"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    seats = booking.seats.all()
    
    return render(request, 'payment.html', {
        'booking': booking,
        'user': request.user,
        'seats': seats
    })


def payment_failed(request, imdb_id):
    """Payment failed page"""
    return render(request, 'payment_failed.html')


@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa callback"""
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            payment_status = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            
            if payment_status == 0:
                # Payment was successful
                print("Payment successful. Proceed.")
            
            response = {'ResultCode': 0, 'ResultDesc': 'Accepted'}
            return JsonResponse(response)
        except json.JSONDecodeError:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Method not allowed'}, status=405)


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('login')


@staff_member_required
def dashboard(request):
    """Admin dashboard"""
    tickets_sold = Booking.objects.count()
    total_users = User.objects.count()
    total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    conversion_rate = (tickets_sold / total_users * 100) if total_users > 0 else 0
    
    return render(request, 'dashboard.html', {
        'tickets_sold': tickets_sold,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'conversion_rate': conversion_rate
    })


@staff_member_required
def dashboard_movies(request):
    """Admin movies page"""
    title = request.GET.get('title', '')
    movies = []
    
    if title:
        movies = search_movies(title)
    else:
        title = random.choice(PREDEFINED_TITLES)
        movies = search_movies(title)
    
    return render(request, 'dashboard_movies.html', {'movies': movies})


@staff_member_required
def dashboard_movie_detail(request, imdb_id):
    """Admin movie detail page"""
    movie_data = get_movie_data(imdb_id)
    if not movie_data:
        return render(request, '404.html', status=404)
    
    movie = Movie.objects.filter(imdb=imdb_id).first()
    showtimes = movie.showtimes.all() if movie else None
    
    return render(request, 'dashboard_movie_detail.html', {
        'movie': movie_data,
        'movie_obj': movie,
        'showtimes': showtimes
    })


@staff_member_required
@require_http_methods(["POST"])
def add_movie_showtime(request, imdb_id):
    """Add showtime for a movie"""
    movie_id = request.POST.get('movie')
    date = request.POST.get('date')
    time_str = request.POST.get('time')
    
    movie = Movie.objects.filter(imdb=movie_id).first()
    if not movie:
        # Fetch movie data from OMDB and create movie
        movie_data = get_movie_data(movie_id)
        if movie_data:
            movie = Movie.objects.create(
                title=movie_data.get('Title'),
                genre=movie_data.get('Genre', ''),
                description=movie_data.get('Plot', ''),
                poster=movie_data.get('Poster', ''),
                imdb=movie_id
            )
        else:
            return HttpResponse("Movie not found", status=404)
    
    # Create showtime
    from datetime import datetime
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    
    Showtime.objects.create(
        movie=movie,
        date=date_obj,
        time=time_obj
    )
    
    return redirect('dashboard_movie_detail', imdb_id=imdb_id)


@staff_member_required
@require_http_methods(["POST"])
def delete_showtime(request, showtime_id):
    """Delete a showtime"""
    showtime = get_object_or_404(Showtime, id=showtime_id)
    movie_imdb = showtime.movie.imdb
    showtime.delete()
    return redirect('dashboard_movie_detail', imdb_id=movie_imdb)


@staff_member_required
def dashboard_bookings(request):
    """Admin bookings page"""
    bookings = Booking.objects.select_related('user', 'showtime', 'payment').prefetch_related('seats').all()
    return render(request, 'dashboard_bookings.html', {'bookings': bookings})


@staff_member_required
def dashboard_users(request):
    """Admin users page"""
    users = User.objects.all()
    return render(request, 'dashboard_users.html', {'users': users})


@staff_member_required
def generate_reports(request):
    """Generate and download PDF report"""
    from booking.management.commands.generate_report import generate_report
    import os
    from django.conf import settings
    
    file_path = os.path.join(settings.BASE_DIR, 'report.pdf')
    try:
        generate_report(file_path)
        
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            return HttpResponse("Report generation failed", status=500)
    except Exception as e:
        return HttpResponse(f"Report generation failed: {str(e)}", status=500)
