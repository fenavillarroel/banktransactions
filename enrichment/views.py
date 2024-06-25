from django.shortcuts import render
from rest_framework import viewsets
from .models import Transaccion, Categoria, Comercio, Keyword
from .serializers import TransaccionSerializer, CategoriaSerializer, ComercioSerializer, KeywordSerializer
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Transaccion, Categoria, Comercio, Keyword
from .serializers import TransaccionSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ComercioViewSet(viewsets.ModelViewSet):
    queryset = Comercio.objects.all()
    serializer_class = ComercioSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer


class EnrichmentAPIView(APIView):
    """
    Enrichment API view.

    Endpoint for enriching transactions with merchant and category information.
    """
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['transactions'],
            properties={
                'transactions': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_STRING),
                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                            'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                        },
                        required=['id', 'description', 'amount', 'date']
                    )
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Enriched transactions",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'transactions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'keyword': openapi.Schema(type=openapi.TYPE_STRING),
                                    'merchant_id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'category_id': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        ),
                        'total_transactions': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'categorization_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'merchant_identification_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        transactions_data = request.data.get('transactions', [])
        enriched_transactions = []
        total_transactions = len(transactions_data)
        categorization_count = 0
        merchant_identification_count = 0

        for transaction in transactions_data:
            description = transaction.get('description', '')
            amount = transaction.get('amount', 0)
            transaction_id = transaction.get('id', str(uuid.uuid4()))

            # Determinar el tipo de transacción (gasto o ingreso)
            if amount < 0:
                transaction_type = 'expense'
            else:
                transaction_type = 'income'

            # Buscar keywords que coincidan con la descripción
            keywords = Keyword.objects.filter(keyword__iexact=description)
            if keywords.exists():
                keyword_obj = keywords.first()
                merchant = keyword_obj.merchant
                merchant_id = merchant.id
                category_id = merchant.category.id if merchant.category else None
                categorization_count += 1
                merchant_identification_count += 1
            else:
                merchant_id = None
                category_id = None

            # Si no se encontró un comercio, se intenta categorizar como ingreso
            if category_id is None and transaction_type == 'income':
                category_id = Categoria.objects.get(type='income').id
                categorization_count += 1

            # Construir la transacción enriquecida
            enriched_transaction = {
                "id": transaction_id,
                "description": description,
                "amount": amount,
                "transaction_type": transaction_type,
                "merchant_id": merchant_id,
                "category_id": category_id
            }
            enriched_transactions.append(enriched_transaction)

            # Persistir la transacción en la base de datos
            Transaccion.objects.create(
                id=transaction_id,
                description=description,
                amount=amount,
                date=transaction.get('date'),
                merchant_id=merchant_id,
                category_id=category_id
            )

        # Calcular métricas
        categorization_rate = (categorization_count / total_transactions) * 100 if total_transactions > 0 else 0
        merchant_identification_rate = (merchant_identification_count / total_transactions) * 100 if total_transactions > 0 else 0

        # Preparar la respuesta
        response_data = {
            "transactions": enriched_transactions,
            "total_transactions": total_transactions,
            "categorization_rate": categorization_rate,
            "merchant_identification_rate": merchant_identification_rate,
        }

        return Response(response_data, status=status.HTTP_200_OK)

