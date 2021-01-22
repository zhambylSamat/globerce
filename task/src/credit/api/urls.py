from django.urls import path
from .views import (
	AuthView,
	HolidayView,
	PaymentDateView,
	ClientView,
)


urlpatterns = [
	path('auth/', AuthView.as_view()),
	path('holidays/', HolidayView.as_view()),
	path('credit/<date>/', PaymentDateView.as_view()),
	path('client/', ClientView.as_view()),
]
