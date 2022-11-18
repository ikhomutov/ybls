from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.levels_list_view),
    path('<int:level>/', views.subjects_list_view, name='subjects-list'),
    path('<int:level>/<int:subject_id>/',views.subject_detail_view, name='subject-detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail_view, name='lesson-detail'),
]
