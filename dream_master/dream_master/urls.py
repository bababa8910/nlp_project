from django.contrib import admin
from django.urls import path
from app01 import views
from app01.views import home_page_view, index_view, category_view
from app01.views import ciyun_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('dream_interpreter/', views.dream_interpreter, name='dream_interpreter'),
    path('category/<str:category>/', views.category_view, name='category'),  # 新增
    path('index/', views.index_view, name='index'),
    path('home/', home_page_view, name='home'),
    path('chat/', views.chat_view, name='chat'),
    path('emotion_analysis/', views.emotion_analysis, name='emotion_analysis'),
    path('dream_analysis/', views.dream_analysis, name='dream_analysis'),
    path('new_view/', views.new_view, name='new_view'),
    path('ciyun/', ciyun_view, name='ciyun'),

]