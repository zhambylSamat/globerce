from rest_framework import serializers


class ClientSerializer(serializers.Serializer):

	fio = serializers.CharField(max_length=200)
	phone = serializers.CharField(max_length=10)
	iin = serializers.IntegerField(max_value=999999999999)
	amount = serializers.DecimalField(decimal_places=2, max_digits=9)
	period = serializers.IntegerField()
	credit_type = serializers.CharField(max_length=1)
