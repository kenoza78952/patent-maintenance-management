from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.login_view, name='login'), 
    path('home/', views.home, name='home'),
    path('calculate/', views.calculate_fees_view, name='calculate_fees'),
    path('fees-dollars/', views.view_fees_dollars, name='view_fees_dollars'),
    path('download-fees/', views.download_fees, name='download_fees'),
    path('upload-fees/', views.upload_fees, name='upload_fees'),
    path('bulk_download/', views.bulk_download, name='bulk_download'),
    path('gpt-categorize/', views.gpt_categorize_view, name='gpt-categorize'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
