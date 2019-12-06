from django.urls import path,include
from . import views

app_name = 'workspace'

urlpatterns = [
########################################################## page url ###############################################
    path('', views.home,name='home'),
    path('log-view', views.log_view, name='log_view'),
    path('log-detail', views.log_detail, name='log_detail'),
    path('review', views.review, name='review'),
    path('edit-script', views.edit_script, name='edit_script'),
    path('source', views.source, name='source'),
###################################################################################################################

    path('crawl-now', views.crawl_now, name='crawl_now'),
    path('delete-log', views.delete_log, name='delete_log'),
    path('save-script', views.save_script, name='save_script'),
    path('get-source', views.get_source, name='get_source'),
    path('approve', views.approve, name='approve'),
    path('send-import', views.send_import, name='send_import'),

    path('approve-record', views.approve_record, name='approve_record'),
    path('save-record', views.save_record, name='save_record'),
    path('send-record', views.send_record, name='send_record'),
    path('delete-record', views.delete_record, name='delete_record'),
    path('cancel-record', views.cancel_record, name='cancel_record'),

]

