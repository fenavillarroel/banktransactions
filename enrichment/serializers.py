from rest_framework import serializers
from .models import Transaccion, Categoria, Comercio, Keyword
import datetime

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, data):
        if 'name' not in data:
            raise serializers.ValidationError("El campo 'name' es obligatorio.")
        if 'type' not in data:
            raise serializers.ValidationError("El campo 'type' es obligatorio.")
        return data
    
class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercio
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }
    
    def validate(self, data):
        if 'merchant_name' not in data:
            raise serializers.ValidationError("El campo 'merchant_name' es obligatorio.")
        return data


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'keyword', 'merchant']

    def validate(self, data):
        if not data.get('keyword'):
            raise serializers.ValidationError("Keyword is required")
        if not data.get('merchant'):
            raise serializers.ValidationError("Merchant is required")
        return data

class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},  # El ID se genera automáticamente
        }

    def validate_amount(self, value):
        if value == 0:
            raise serializers.ValidationError("El campo 'amount' no puede ser cero.")
        return value

    def validate_date(self, value):
        try:
            # Intenta parsear la fecha para asegurarte de que sea válida
            datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError("Formato de fecha inválido. Utiliza el formato YYYY-MM-DD.")
        return value