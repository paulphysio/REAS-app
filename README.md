# REAS-app
*Student Results Emailer*
This web app allows users to upload an Excel file containing student results, and automatically sends the results to each student's email address.

*Getting Started*
To use this app, simply upload an Excel file containing the following columns:

"Email": the email address of the student
"Name": the name of the student
"Result": the student's result (e.g. "Pass" or "Fail")
The app will then extract the information from the Excel file and use it to send an email to each student containing their results.


Built With
Django - The web framework used
Google API Client Library for Python - Used for sending the emails via the Gmail API
Pandas - Used for reading and manipulating the Excel file
