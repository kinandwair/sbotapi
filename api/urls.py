from django.urls import path

from api import AggAPI
from . import views

urlpatterns = [
    path('', views.index, name='search'),
    path('v1/property/', views.search, name='index'),
    path('v1/cars/', views.carsearch, name='index'),
    path('v1/averagePricePerArea/', AggAPI.averagePricePerArea, name='index'),
    path('v1/averagePricePerBuildingForSpecificAreaAndSize/', AggAPI.averagePricePerBuildingForSpecificAreaAndSize, name='index'),
    path('v1/averagePricePerSizeForSecificArea/', AggAPI.averagePricePerSizeForSecificArea, name='index'),
    path('v1/averagePricesPerAreaPerSizeForSpecificCoordinates/', AggAPI.averagePricesPerAreaPerSizeForSpecificCoordinates, name='index'),
    path('v1/whatAreTheAveragePricesInSpecificBuilding/', AggAPI.whatAreTheAveragePricesInSpecificBuilding, name='index'),
    path('v1/propertiesInCityPerBudget/', AggAPI.propertiesInCityPerBudget, name='index'),
    path('v1/averagePricePerAreaForSpecificSize/', AggAPI.averagePricePerAreaForSpecificSize, name='index'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='search'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('/property/', PropertyRoute.post, name='property'),
]