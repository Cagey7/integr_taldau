from django.urls import path
from . import views

urlpatterns = [
    path('chapters/', views.GetAllChapters.as_view()),
    path('indices/', views.GetAllIndices.as_view()),
    path('periods-dics/<int:index_id>', views.GetPeriodsDicsById.as_view()),
    path('index-data/<int:index_id>', views.GetIndexData.as_view())
]