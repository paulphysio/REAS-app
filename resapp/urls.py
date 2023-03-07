from django.urls import path
from .views import guidesView, homeView, activityFormView, detailView, deleteView, aboutView, questionAskedView, aboutUsView, handler404, handler500
from django.conf.urls import handler404, handler500

handler404 = 'resapp.views.handler404'
handler500 = 'resapp.views.handler500'
urlpatterns = [
    path('home/', homeView, name='home' ),
    path('', aboutView, name='about' ),
    path('about_us', aboutUsView, name='about_us' ),
    path('guides', guidesView, name='guides' ),
    path('ask/', questionAskedView, name = "question"),
    path('save/', activityFormView, name='activity_form' ),
    path('file/<int:pk>', detailView, name='file_details' ),
    path('delete/file/<int:pk>', deleteView, name="delete_file")
]