from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .services import get_holidays, get_holiday_by_date
from datetime import datetime
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class AuthView(ObtainAuthToken):
	permission_classes = (AllowAny,)

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,
										   context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'token': token.key,
			'user_id': user.pk
		})


class HolidayView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):
		result = get_holidays()
		return Response(result, status=200)


class PaymentDateView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request, date):
		choosen_date = datetime.strptime(date, '%Y-%m-%d').date()
		holiday = get_holiday_by_date(choosen_date)
		if holiday is not None:
			result = {'message': 'Выберите другую дату. {holiday_date}'.format(holiday_date=holiday['name'])}
			return Response(result, status=200)
		else:
			if 'date' in cache:
				result = {'message': 'ok in cache'}
			else:
				cache.set('date', date, timeout=CACHE_TTL)
				result = {'message': 'ok set to cache'}
			return Response(result, status=200)


class ClientView(APIView):
	permission_classes = (IsAuthenticated,)

	def post(self, request):
		if 'clients' not in cache:
			cache.set('clients', {}, timeout=CACHE_TTL)
		if request.data['iin'] not in cache.get('clients'):
			cache_clients = cache.get('clients')
			cache_clients[request.data['iin']] = {'fio': request.data['fio'],
												'phone': request.data['phone'],
												'amount': request.data['amount'],
												'period': request.data['period'],
												'credit_type': request.data['credit_type']}
			cache.set('clients', cache_clients, timeout=CACHE_TTL)
			print(cache.get('clients'))
		return Response(status=200)
