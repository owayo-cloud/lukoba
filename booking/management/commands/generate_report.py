from django.core.management.base import BaseCommand
from booking.models import User, Movie, Showtime, Seat, Booking, Payment
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib import colors
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta
from django.utils import timezone


def generate_report(filename):
    """Generate PDF report"""
    # Create a PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        name='Title', fontSize=22, alignment=1, spaceAfter=24, fontName='Helvetica-Bold')

    # Heading style
    heading_style = ParagraphStyle(
        name='Heading', fontSize=16, fontName='Helvetica-Bold', spaceAfter=12)

    # Normal text style
    normal_style = styles['BodyText']
    normal_style.fontName = 'Helvetica'
    normal_style.fontSize = 10
    normal_style.leading = 12
    normal_style.alignment = 0

    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('WORDWRAP', (0, 1), (-1, -1), True),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ])

    # Create a list to hold the elements
    elements = []

    # Add title
    elements.append(Paragraph("Lukoba Online Movie Ticket Booking System Report", title_style))

    # Add Users section
    elements.append(Paragraph("Users", heading_style))
    user_data = [['ID', 'Username', 'Email', 'Admin']]
    for user in User.objects.all():
        user_data.append([
            user.id,
            user.username,
            user.email,
            'Yes' if user.is_admin else 'No'
        ])

    user_table = Table(user_data, colWidths=[0.5*inch, 2.5*inch, 2.5*inch, 1*inch])
    user_table.setStyle(table_style)
    elements.append(user_table)
    elements.append(PageBreak())

    # Add Movies section
    elements.append(Paragraph("Movies", heading_style))
    movie_data = [['ID', 'Title', 'Genre', 'IMDB ID']]
    for movie in Movie.objects.all():
        movie_data.append([
            movie.id,
            movie.title[:30] + '...' if len(movie.title) > 30 else movie.title,
            movie.genre[:20] + '...' if len(movie.genre) > 20 else movie.genre,
            movie.imdb
        ])

    movie_table = Table(movie_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    movie_table.setStyle(table_style)
    elements.append(movie_table)
    elements.append(PageBreak())

    # Add Showtimes section
    elements.append(Paragraph("Showtimes", heading_style))
    showtime_data = [['ID', 'Movie Title', 'Date', 'Time', 'Seats Available']]
    for showtime in Showtime.objects.select_related('movie').all():
        movie_title = showtime.movie.title
        movie_title = movie_title[:30] + '...' if len(movie_title) > 30 else movie_title
        showtime_data.append([
            showtime.id,
            movie_title,
            showtime.date.strftime('%Y-%m-%d'),
            showtime.time.strftime('%H:%M:%S'),
            showtime.seats_available
        ])

    showtime_table = Table(showtime_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.25*inch, 1.25*inch])
    showtime_table.setStyle(table_style)
    elements.append(showtime_table)
    elements.append(PageBreak())

    # Add Bookings section
    elements.append(Paragraph("Bookings", heading_style))
    booking_data = [['ID', 'User', 'Movie', 'Seats Booked', 'Total Cost']]
    for booking in Booking.objects.select_related('user', 'showtime__movie', 'payment').prefetch_related('seats').all():
        movie_title = booking.showtime.movie.title
        movie_title = movie_title[:30] + '...' if len(movie_title) > 30 else movie_title
        seats_booked = booking.seats.count()
        total_cost = booking.payment.amount if booking.payment else seats_booked * 200
        booking_data.append([
            booking.id,
            booking.user.username,
            movie_title,
            seats_booked,
            f"Ksh {total_cost:.2f}"
        ])

    booking_table = Table(booking_data, colWidths=[0.5*inch, 2*inch, 2*inch, 1.5*inch, 1.5*inch])
    booking_table.setStyle(table_style)
    elements.append(booking_table)
    elements.append(PageBreak())

    # Add Payment section
    elements.append(Paragraph("Payments Report", heading_style))
    payments = Payment.objects.all()
    data = [['Payment ID', 'Amount', 'Payment Method', 'Transaction ID']]
    for payment in payments:
        data.append([
            payment.id,
            f"Ksh {payment.amount:.2f}",
            payment.payment_method,
            payment.transaction_id
        ])

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    # Add Total Revenue section
    elements.append(Paragraph("Total Revenue", heading_style))
    total_revenue = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    revenue_data = [['Total Revenue'], [f"Ksh {total_revenue:.2f}"]]
    revenue_table = Table(revenue_data, colWidths=[4*inch])
    revenue_table.setStyle(table_style)
    elements.append(revenue_table)
    elements.append(PageBreak())

    # Add Seats Availability section
    elements.append(Paragraph("Seats Availability", heading_style))
    seat_data = [['Showtime ID', 'Total Seats', 'Available Seats', 'Booked Seats']]
    for showtime in Showtime.objects.all():
        total_seats = Seat.objects.filter(showtime=showtime).count()
        booked_seats = Seat.objects.filter(showtime=showtime, is_booked=True).count()
        available_seats = showtime.seats_available
        seat_data.append([
            showtime.id,
            total_seats,
            available_seats,
            booked_seats
        ])

    seat_table = Table(seat_data, colWidths=[0.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    seat_table.setStyle(table_style)
    elements.append(seat_table)
    elements.append(PageBreak())

    # Add Movies with Highest Bookings section
    elements.append(Paragraph("Movies with Highest Bookings", heading_style))
    highest_booking_data = [['Movie Title', 'Total Bookings']]
    
    # Get movies with booking counts
    movies_with_bookings = Movie.objects.annotate(
        booking_count=Count('showtimes__bookings')
    ).filter(booking_count__gt=0).order_by('-booking_count')[:10]
    
    for movie in movies_with_bookings:
        movie_title = movie.title[:30] + '...' if len(movie.title) > 30 else movie.title
        highest_booking_data.append([
            movie_title,
            movie.booking_count
        ])

    highest_booking_table = Table(highest_booking_data, colWidths=[2.5*inch, 1.5*inch])
    highest_booking_table.setStyle(table_style)
    elements.append(highest_booking_table)
    elements.append(PageBreak())

    # Add Upcoming Showtimes section
    elements.append(Paragraph("Upcoming Showtimes", heading_style))
    upcoming_date = timezone.now().date() + timedelta(days=7)
    upcoming_showtime_data = [['ID', 'Movie Title', 'Date', 'Time', 'Seats Available']]
    
    upcoming_showtimes = Showtime.objects.filter(
        date__gte=timezone.now().date(),
        date__lte=upcoming_date
    ).select_related('movie').all()
    
    for showtime in upcoming_showtimes:
        movie_title = showtime.movie.title
        movie_title = movie_title[:30] + '...' if len(movie_title) > 30 else movie_title
        upcoming_showtime_data.append([
            showtime.id,
            movie_title,
            showtime.date.strftime('%Y-%m-%d'),
            showtime.time.strftime('%H:%M:%S'),
            showtime.seats_available
        ])

    upcoming_showtime_table = Table(upcoming_showtime_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.25*inch, 1.25*inch])
    upcoming_showtime_table.setStyle(table_style)
    elements.append(upcoming_showtime_table)

    # Build PDF
    doc.build(elements)
    return filename


class Command(BaseCommand):
    help = 'Generate a PDF report from the database'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='report.pdf',
                          help='Output filename for the PDF report')

    def handle(self, *args, **options):
        output_file = options.get('output', 'report.pdf')
        try:
            generate_report(output_file)
            self.stdout.write(self.style.SUCCESS(f'Report generated: {output_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to generate report: {str(e)}'))
