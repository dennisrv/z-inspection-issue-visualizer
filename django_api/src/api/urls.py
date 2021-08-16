from django.urls import path

from . import views

urlpatterns = [
    path('auth', views.AuthView.as_view(), name='auth'),
    path('nodes/', views.NodesIndexView.as_view(), name='index'),
    path('nodes/<int:node_id>', views.NodeDetailView.as_view(), name='detail')
]