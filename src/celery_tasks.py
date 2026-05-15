from celery import Celery
from src.config import my_config
from src.mail import the_mail, create_verification_message
from asgiref.sync import async_to_sync

my_celery_app = Celery(
    __name__ = "Email Tasks",
    broker= my_config.BROKER_URL,
    backend= my_config.RESULTS_BACKEND_URL
)

@my_celery_app.task()
def send_the_email(email, subject, name, link):
    my_message = create_verification_message(
        the_recipients= [email],
        the_subject= subject,
        the_name= name,
        the_link= link
    )

    async_to_sync(the_mail.send_message)(
        message=my_message,
        template_name="verification_email.html",
    )
    
    return f"Message sent to {name} successfully!"
    
    

