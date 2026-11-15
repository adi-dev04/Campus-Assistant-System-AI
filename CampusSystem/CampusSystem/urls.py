from django.contrib import admin
from django.urls import path, include
from CampusSystem import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('tlogin/', views.tlogin_view, name='tlogin'),
    path('studentportal/', views.student_portal_view, name='student_portal'),
    path('syllabus/', views.syllabus_view, name='syllabus'),
    path('notice/', views.notice_view, name='notice'),
    path('timetable/', views.timetable_view, name='timetable'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('extract_pdf_text/<int:document_id>/', views.extract_pdf_text, name='extract_pdf_text'),
    path('student_documents/', views.student_documents, name='student_documents'),
    path('document_detail/<int:document_id>/', views.document_detail, name='document_detail'),
    path('upload-pdf/', views.upload_syllabus, name='upload_pdf'),
    path('upload-notice/', views.upload_notice, name='upload_notice'),
    path('upload-timetable/',views.upload_timetable, name='upload_timetable'),
    path('delete-upload/<int:document_id>/', views.delete_upload, name='delete_upload'),
    path('manage_uploads/', views.manage_uploads, name='manage_uploads'),
    path('ask-qwen/', views.ask_qwen, name='ask_qwen'),
    path('test-qwen/', views.test_qwen, name='test_qwen'),
    ]