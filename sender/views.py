from django.http import HttpResponseRedirect
from django.shortcuts import render
import pandas as pd
import openpyxl as op
import smtplib, ssl
from email.message import EmailMessage
from resapp.models import activity
from .models import emailSender
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading
import concurrent.futures
# Create your views here.
def sendMail(request, pk):
    if request.method == 'POST':
        activity_detail = activity.objects.get(id=pk)
        sheet = activity_detail.file_uploaded
        df = pd.read_excel(sheet)

        email_column = next((c for c in ['Email', 'EMAIL', 'email'] if c in df.columns), None)
        if email_column is None:
            print('Error: Email column not found')
            return HttpResponseRedirect("/home")

        recipients = df[email_column].tolist()
        messages = [df.iloc[i].to_dict() for i in range(len(df))]

        def send_email(recipient, subject, body):
            try:
                port = 465
                email = 'emilyjohnson25099@gmail.com'
                password = "wlwzkvalbpwebxot"
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login(email, password)
                    message = MIMEMultipart()
                    message['From'] = 'The Course Adviser'
                    message['To'] = recipient
                    message['Subject'] = subject
                    body_part = MIMEText(body, 'plain')
                    message.attach(body_part)
                    server.sendmail(email, recipient, message.as_string())
                print('Email sent to {}'.format(recipient))
            except Exception as e:
                print('Error: {}'.format(e))

        def send_emails_with_threads():
            num_threads = 7
            threads = []
            chunk_size = len(recipients) // num_threads
            for i in range(num_threads):
                start = i * chunk_size
                end = start + chunk_size
                if i == num_threads - 1:
                    end = len(recipients)
                chunk_receivers = recipients[start:end]
                chunk_messages = messages[start:end]
                t = threading.Thread(target=send_chunk_emails, args=(chunk_receivers, chunk_messages))
                threads.append(t)
            start_time = time.time()
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            time_taken = time.time() - start_time
            print(f"Sent {len(recipients)} emails in {time_taken} seconds.")

        def send_chunk_emails(receivers, messages):
            for i in range(len(receivers)):
                send_email(receivers[i], "Harmattan semester results", str(messages[i]))

        send_emails_with_threads()

        sender = request.user
        email_sender_list = [emailSender(sender=sender, receiver_email=recipient, message_sent=message) for recipient, message in zip(recipients, messages)]
        emailSender.objects.bulk_create(email_sender_list)

        return HttpResponseRedirect("/home")

    return render(request, 'send_mail.html')
