from django.urls import path

from . import views

urlpatterns = [
    path('auth', views.AuthView.as_view(), name='auth'),
    path('nodes/', views.IndexView.as_view(), name='issue-index'),
    path('nodes/<int:node_id>', views.IssueDetailView.as_view(), name='issue-detail'),
    path('nodes/merge', views.MergeView.as_view(), name='merge'),
    path('nodes/import', views.ImportView.as_view(), name='import'),
]