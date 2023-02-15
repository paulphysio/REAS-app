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
    
    def send_email(recipient, body):
        try:
            port = 465
            email = 'emilyjohnson25099@gmail.com'
            password = "wlwzkvalbpwebxot"
            context = ssl.create_default_context()
            server=smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
            server.login(email, password)
            em = MIMEMultipart("alternative")
            em['From'] = 'The Course Adviser'
            em['To'] = receiver
            em['Subject'] = "Harmattan semester results"
            # for receiverr, message in zip(receiver_list, reallist):
            server.sendmail(email, str(recipient), str(body))
            server.quit()
            print('Email sent to {}'.format(recipient))
        except Exception as e:
            print('Error: {}'.format(e))
    
    counter=0
    activity_detail = activity.objects.get(id=pk)
    sheet = activity_detail.file_uploaded
    df = pd.read_excel(sheet)
    wb = op.load_workbook(sheet)
    wa = wb.active
    if df.columns.get_loc('Email'):
        email_index = df.columns.get_loc('Email')
    elif df.columns.get_loc('EMAIL'):
        email_index = df.columns.get_loc('EMAIL')
    elif df.columns.get_loc('email'):
        email_index = df.columns.get_loc('email')
    reallist = []
    f_msg = []
    for i in range(1, wa.max_row+1):
        lister=[]
        for j in range(1, wa.max_column+1):
            cell_obj = wa.cell(row=i, column=j)
            y = wa.cell(row=1, column=j).value
            lister.append(y)
            if j==(wa.max_column):
                f_msg.append(lister)
                
    receiver_list=[]
    for i in range(2, wa.max_row+1):
        list=[]
        if counter <= 20:

            for j in range(1, wa.max_column+1):
                cell_obj = wa.cell(row=i, column=j)
                x = wa.cell(row=i, column=j).value
                list.append(x)
                if j==(wa.max_column):
                    reallist.append(list)
                    
            receiver = str(wa.cell(row=i, column=email_index+ 1).value)
            receiver_list.append(receiver)

        else:
            # Add a delay of 1 minute if the counter is over 20
            time.sleep(5)
            counter = 0
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
        for i in range(len(receiver_list)):
            recipient = receiver_list[i]
            body = reallist[i]
            executor.submit(send_email, recipient, body)
    

    print('All emails sent.')
    
    if request.method == 'POST':

        sender = request.user
        receiver_email = receiver
        message_sent = reallist

        emailSender(sender=sender, receiver_email = receiver_email, message_sent = message_sent).save()
    return HttpResponseRedirect("/home")
