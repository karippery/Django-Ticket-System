from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@shared_task
def send_ticket_created_email(ticket_id, user_email):
    subject = 'Your ticket has been created'
    html_message = render_to_string('emails/ticket_created.html', {
        'ticket_id': ticket_id,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
    )


@shared_task
def send_ticket_updated_email(ticket_id, user_email, status):
    subject = f'Your ticket #{ticket_id} has been updated'
    html_message = render_to_string('emails/ticket_updated.html', {
        'ticket_id': ticket_id,
        'status': status,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
    )


@shared_task
def send_comment_notification(ticket_id, user_email, comment_author):
    subject = f'New comment on ticket #{ticket_id}'
    html_message = render_to_string('emails/new_comment.html', {
        'ticket_id': ticket_id,
        'comment_author': comment_author,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
    )
