from django.urls import path
from . import views
from .folder_of_views.admin_views import *
from .services.file_creator import *
from .folder_of_views.admin_pivot_views import *

urlpatterns = [
    path("", views.home_view, name='home'),
    path("formkpi/", views.cards_update_view, name='update'),
    path("pivot/", views.PivotCardView.as_view(), name='user_pivot'),
    path("adminpivot/", AdminPivotView.as_view(), name='admin_pivot'),
    # path("admin/", AdminPivotView.as_view(), name='admin_pivot'),
#    path("admin/", admin_cards_update_view, name='admin_pivot'),
    path("onchecking/", OnCheckinView.as_view(), name='onchecking'),
    path("download/", download_excel_data, name='download_pivot'),
    path("notfixdate/", download_excel_data_without, name='download_pivot_not_fix'),
    path("close/", close_edit, name='close'),
    path("open/", open_edit, name='open'),
    path('<int:pk>/accept/', accept_kpi, name='accept'),
    path('<int:pk>/reject/', reject_kpi, name='reject'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('export-pdf', views.export_pdf, name="export-pdf"),


]