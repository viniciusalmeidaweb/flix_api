from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.MovieCreateListview.as_view(), name='movie-create-list'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyView.as_view(), name='movie-detail-view'),
    path('movies/stats/', views.MovieStatsView.as_view(), name='movie-stats-view'),
]