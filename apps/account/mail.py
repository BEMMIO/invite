import threading

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    """
    Class for send email async with thread.
    """
    def __init__(self, subject, body, from_email, recipient_list,
                 fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        # Check if the email smtp is configurated
        if (settings.EMAIL_HOST
                and settings.EMAIL_HOST_PASSWORD):
            msg = EmailMultiAlternatives(
                self.subject, self.body, self.from_email, self.recipient_list
            )
            if self.html:
                msg.attach_alternative(self.html, "text/html")
            msg.send(self.fail_silently)


def send_mail(subject, body, from_email, recipient_list, fail_silently=False,
              html=None, *args, **kwargs):
    """
    Send email async.
    """
    EmailThread(
        subject, body, from_email, recipient_list, 
        fail_silently, html
    ).start()



'''
@use:
			send_mail(
				subject,
				body,
				from_email,
				[to_email],
				)

'''