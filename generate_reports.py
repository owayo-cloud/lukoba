import argparse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib import colors
from db_setup import SessionLocal
from models import User, Movie, Showtime, Seat, Booking, Payment
from sqlalchemy import func
from datetime import datetime, timedelta

# Initialize database session
db = SessionLocal()


def generate_report(filename):
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
    for user in db.query(User).all():
        user_data.append([user.id, user.username, user.email,
                         'Yes' if user.is_admin else 'No']) # type: ignore

    user_table = Table(user_data, colWidths=[
                       0.5*inch, 2.5*inch, 2.5*inch, 1*inch])
    user_table.setStyle(table_style)
    elements.append(user_table)
    elements.append(PageBreak())

    # Add Movies section
    elements.append(Paragraph("Movies", heading_style))
    movie_data = [['ID', 'Title', 'Genre', 'IMDB ID']]
    for movie in db.query(Movie).all():
        movie_data.append([
            movie.id,
            movie.title[:30] + '...' if len(movie.title) > 30 else movie.title, # type: ignore
            movie.genre[:20] + '...' if len(movie.genre) > 20 else movie.genre, # type: ignore
            movie.imdb
        ])

    movie_table = Table(movie_data, colWidths=[
                        0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    movie_table.setStyle(table_style)
    elements.append(movie_table)
    elements.append(PageBreak())

    # Add Showtimes section
    elements.append(Paragraph("Showtimes", heading_style))
    showtime_data = [['ID', 'Movie Title', 'Date', 'Time', 'Seats Available']]
    for showtime in db.query(Showtime).all():
        movie_title = db.query(Movie).filter(Movie.id == showtime.movie_id).first().title[:30] + '...' if len(db.query(Movie).filter( # type: ignore
            Movie.id == showtime.movie_id).first().title) > 30 else db.query(Movie).filter(Movie.id == showtime.movie_id).first().title # type: ignore
        showtime_data.append([
            showtime.id,
            movie_title,
            showtime.date.strftime('%Y-%m-%d'),
            showtime.time.strftime('%H:%M:%S'),
            showtime.seats_available
        ]) # type: ignore

    showtime_table = Table(showtime_data, colWidths=[
                           0.5*inch, 2.5*inch, 1.5*inch, 1.25*inch, 1.25*inch])
    showtime_table.setStyle(table_style)
    elements.append(showtime_table)
    elements.append(PageBreak())

    # Add Bookings section
    elements.append(Paragraph("Bookings", heading_style))
    booking_data = [['ID', 'User', 'Movie', 'Seats Booked', 'Total Cost']]
    for booking in db.query(Booking).all():
        user = db.query(User).filter(
            User.id == booking.user_id).first().username # type: ignore
        movie_title = db.query(Movie).filter(Movie.id == db.query(Showtime).filter(Showtime.id == booking.showtime_id).first().movie_id).first().title[:30] + '...' if len(db.query(Movie).filter(Movie.id == db.query(Showtime).filter( # type: ignore
            Showtime.id == booking.showtime_id).first().movie_id).first().title) > 30 else db.query(Movie).filter(Movie.id == db.query(Showtime).filter(Showtime.id == booking.showtime_id).first().movie_id).first().title # type: ignore
        seats_booked = db.query(Seat).filter(
            Seat.booking_id == booking.id).count()
        total_cost = seats_booked * 200
        booking_data.append([
            booking.id,
            user,
            movie_title,
            seats_booked,
            total_cost
        ]) # type: ignore

    booking_table = Table(booking_data, colWidths=[
                          0.5*inch, 2*inch, 2*inch, 1.5*inch, 1.5*inch])
    booking_table.setStyle(table_style)
    elements.append(booking_table)
    elements.append(PageBreak())

    #Add Payment section
    elements.append(Paragraph("Payments Report", heading_style))
    payments = db.query(Payment).all()
    data = [['Payment ID', 'Amount', 'Payment Method', 'Transaction ID']]
    for payment in payments:
        data.append([payment.id, f"Ksh{payment.amount:.2f}", payment.payment_method, payment.transaction_id]) # type: ignore

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    # Add Total Revenue section
    elements.append(Paragraph("Total Revenue", heading_style))
    total_revenue = db.query(Booking).join(Seat).count() * 200
    revenue_data = [['Total Revenue'], [f"{total_revenue} Shillings"]]
    revenue_table = Table(revenue_data, colWidths=[4*inch])
    revenue_table.setStyle(table_style)
    elements.append(revenue_table)
    elements.append(PageBreak())

    # Add Seats Availability section
    elements.append(Paragraph("Seats Availability", heading_style))
    seat_data = [['Showtime ID', 'Total Seats',
                  'Available Seats', 'Booked Seats']]
    for showtime in db.query(Showtime).all():
        total_seats = db.query(Seat).filter(
            Seat.showtime_id == showtime.id).count()
        booked_seats = db.query(Seat).filter(
            Seat.showtime_id == showtime.id, Seat.is_booked == True).count()
        available_seats = total_seats - booked_seats
        seat_data.append([
            showtime.id,
            total_seats,
            available_seats,
            booked_seats
        ]) # type: ignore

    seat_table = Table(seat_data, colWidths=[
                       0.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    seat_table.setStyle(table_style)
    elements.append(seat_table)
    elements.append(PageBreak())

    # Add Movies with Highest Bookings section
    elements.append(Paragraph("Movies with Highest Bookings", heading_style))
    movie_bookings = db.query(Movie).join(Showtime).join(Booking).join(
        Seat).group_by(Movie.id).order_by(func.count(Seat.id).desc()).all()
    highest_booking_data = [['Movie Title', 'Total Bookings']]
    for movie in movie_bookings:
        total_bookings = db.query(Booking).join(Seat).filter(Seat.showtime_id.in_(
            [showtime.id for showtime in db.query(Showtime).filter(Showtime.movie_id == movie.id).all()])).count()
        highest_booking_data.append([
            movie.title[:30] + '...' if len(movie.title) > 30 else movie.title, # type: ignore
            total_bookings
        ])

    highest_booking_table = Table(
        highest_booking_data, colWidths=[2.5*inch, 1.5*inch])
    highest_booking_table.setStyle(table_style)
    elements.append(highest_booking_table)
    elements.append(PageBreak())

    # Add Upcoming Showtimes section
    elements.append(Paragraph("Upcoming Showtimes", heading_style))
    upcoming_date = datetime.now() + timedelta(days=7)
    upcoming_showtime_data = [
        ['ID', 'Movie Title', 'Date', 'Time', 'Seats Available']]
    for showtime in db.query(Showtime).filter(Showtime.date >= datetime.now().date(), Showtime.date <= upcoming_date.date()).all():
        movie_title = db.query(Movie).filter(Movie.id == showtime.movie_id).first().title[:30] + '...' if len(db.query(Movie).filter( # type: ignore
            Movie.id == showtime.movie_id).first().title) > 30 else db.query(Movie).filter(Movie.id == showtime.movie_id).first().title # type: ignore
        upcoming_showtime_data.append([
            showtime.id,
            movie_title,
            showtime.date.strftime('%Y-%m-%d'),
            showtime.time.strftime('%H:%M:%S'),
            showtime.seats_available
        ]) # type: ignore

    upcoming_showtime_table = Table(upcoming_showtime_data, colWidths=[
                                    0.5*inch, 2.5*inch, 1.5*inch, 1.25*inch, 1.25*inch])
    upcoming_showtime_table.setStyle(table_style)
    elements.append(upcoming_showtime_table)

    # Build PDF
    doc.build(elements)
    print(f"Report generated: {filename}")

# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Generate a report from the database")
    parser.add_argument('--output', type=str, required=True,
                        help="Output filename for the PDF report")
    args = parser.parse_args()
    generate_report(args.output)


if __name__ == "__main__":
    main()
