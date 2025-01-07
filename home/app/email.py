
from datetime import datetime, timedelta, time
from django.core.mail import send_mail
from .models import Appointment
from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.schedulers import DjangoJobScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings



def send_reminder_email(appointment):
    subject = 'Reminder: Your appointment with  Sila Estates'
    message = f'Your appointment with  Sila Estates is scheduled for {appointment.Date}.'
    recipient_email = appointment.Email

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],          
    )

def check_appointments():
    print("Checking appointments...")
    today = datetime.now().date()
    print("Today's date is:", today) 
    
    # Get appointments for today and upcoming appointments
    appointments = Appointment.objects.filter(Date__gte=today).order_by('Date')
    
    for appointment in appointments:
        days_remaining = (appointment.Date - today).days
        print(f"Days remaining for appointment on {appointment.Date}: {days_remaining}")
            
        if days_remaining == 2 or days_remaining == 1:
            send_reminder_email(appointment)
            print(f'Reminder email sent {days_remaining} days before appointment on {appointment.Date}.')

        elif days_remaining == 0:
            send_reminder_email_on_appointment_day(appointment)
            print(f'Reminder email sent on the day of appointment: {appointment.Date}.')


def send_reminder_email_on_appointment_day(appointment):
    subject = 'Reminder: Your appointment with Sila Estates'
    message = f'Your appointment with Sila Estates is scheduled for today ({appointment.Date}).'
    recipient_email = appointment.Email

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
    )


def hello_words():
    print("this is the testing purpose")           

# scheduler = DjangoJobScheduler()
# scheduler = BackgroundScheduler()


# scheduler.add_job(
#     # check_appointments,
#     hello_words,
#     trigger='cron',
#     # hour=9,
#     minute=1,
#     id='check_appointments', 
#     replace_existing=True,
# )

# scheduler.add_job(
#     check_appointments,
#     trigger='interval',  
#     seconds=5,          
#     id='check_appointments', 
#     replace_existing=True,
# )

# def start():
#     scheduler = BackgroundScheduler()
#     viewSets = hello_words()
#     scheduler.add_job(viewSets.getTrackingDetails(), 'interval', minutes=1,replace_existing=True)
# scheduler.start()


try:
    scheduler = BackgroundScheduler(daemon=True)
    # sched.add_job(demo_job, trigger='interval', minutes=1)
    scheduler.add_job(
    hello_words,
    trigger='cron',
    minute='*/1',
    hour='*'
)
    scheduler.start()
    # atexit.register(lambda: sched.shutdown(wait=False))
except:
    print("Unexpected error:")