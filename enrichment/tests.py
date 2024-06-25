from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Categoria, Comercio, Keyword
import uuid

class CategoriaTests(APITestCase):
    def setUp(self):
        self.categoria_url = reverse('categoria-list')
        self.categoria_data = {
            "id": str(uuid.uuid4()),
            "name": "Entretenimiento & Recreación",
            "type": "expense"
        }

    def test_create_categoria(self):
        response = self.client.post(self.categoria_url, self.categoria_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(Categoria.objects.get().name, "Entretenimiento & Recreación")

    def test_get_categorias(self):
        Categoria.objects.create(**self.categoria_data)
        response = self.client.get(self.categoria_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Entretenimiento & Recreación")

    def test_update_categoria(self):
        categoria = Categoria.objects.create(**self.categoria_data)
        update_data = {"name": "Entretenimiento", "type": "expense"}
        url = reverse('categoria-detail', args=[categoria.id])
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categoria.refresh_from_db()
        self.assertEqual(categoria.name, "Entretenimiento")

    def test_delete_categoria(self):
        categoria = Categoria.objects.create(**self.categoria_data)
        url = reverse('categoria-detail', args=[categoria.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Categoria.objects.count(), 0)

class ComercioTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            id=uuid.uuid4(),
            name="Entretenimiento & Recreación",
            type="expense"
        )
        self.comercio = Comercio.objects.create(
            id=uuid.uuid4(),
            merchant_name="Netflix",
            merchant_logo="http://example.com/netflix.png",
            category=self.categoria
        )
        self.valid_payload = {
            "merchant_name": "Spotify",
            "merchant_logo": "http://example.com/spotify.png",
            "category": str(self.categoria.id)
        }
        self.invalid_payload = {
            "merchant_name": "",
            "merchant_logo": "http://example.com/spotify.png",
            "category": str(self.categoria.id)
        }

    def test_get_comercios(self):
        response = self.client.get(reverse('comercio-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Comercio.objects.count())

    def test_get_comercio(self):
        response = self.client.get(reverse('comercio-detail', kwargs={'pk': self.comercio.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['merchant_name'], self.comercio.merchant_name)

    def test_create_comercio(self):
        response = self.client.post(reverse('comercio-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comercio.objects.count(), 2)

    def test_create_comercio_invalid(self):
        response = self.client.post(reverse('comercio-list'), data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comercio.objects.count(), 1)

    def test_update_comercio(self):
        update_payload = {
            "merchant_name": "Netflix Updated",
            "merchant_logo": "http://example.com/netflix_updated.png",
            "category": str(self.categoria.id)
        }
        response = self.client.put(reverse('comercio-detail', kwargs={'pk': self.comercio.id}), data=update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comercio.refresh_from_db()
        self.assertEqual(self.comercio.merchant_name, update_payload['merchant_name'])

    def test_delete_comercio(self):
        response = self.client.delete(reverse('comercio-detail', kwargs={'pk': self.comercio.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comercio.objects.count(), 0)
        
class KeywordTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            id=uuid.uuid4(),
            name="Entretenimiento & Recreación",
            type="expense"
        )
        self.comercio = Comercio.objects.create(
            id=uuid.uuid4(),
            merchant_name="Netflix",
            merchant_logo="http://example.com/netflix.png",
            category=self.categoria
        )
        self.keyword = Keyword.objects.create(
            id=uuid.uuid4(),
            keyword="netflix",
            merchant=self.comercio
        )
        self.valid_payload = {
            "keyword": "spotify",
            "merchant": str(self.comercio.id)
        }
        self.invalid_payload = {
            "keyword": "",
            "merchant": str(self.comercio.id)
        }

    def test_get_keywords(self):
        response = self.client.get(reverse('keyword-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Keyword.objects.count())

    def test_get_keyword(self):
        response = self.client.get(reverse('keyword-detail', kwargs={'pk': self.keyword.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['keyword'], self.keyword.keyword)

    def test_create_keyword(self):
        response = self.client.post(reverse('keyword-list'), data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Keyword.objects.count(), 2)

    def test_create_keyword_invalid(self):
        response = self.client.post(reverse('keyword-list'), data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Keyword.objects.count(), 1)

    def test_update_keyword(self):
        update_payload = {
            "keyword": "netflix_updated",
            "merchant": str(self.comercio.id)
        }
        response = self.client.put(reverse('keyword-detail', kwargs={'pk': self.keyword.id}), data=update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.keyword.refresh_from_db()
        self.assertEqual(self.keyword.keyword, update_payload['keyword'])

    def test_delete_keyword(self):
        response = self.client.delete(reverse('keyword-detail', kwargs={'pk': self.keyword.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Keyword.objects.count(), 0)


class EnrichmentTests(APITestCase):
    def setUp(self):
        self.categoria_income = Categoria.objects.create(name='Income Category', type='income')

    def test_enrichment(self):
        data = {
            "transactions": [
                {"id": uuid.uuid4(), "description": "Expense transaction", "date": "2023-12-01", "amount": -100.00},
                {"id": uuid.uuid4(), "description": "Income transaction", "date": "2023-12-02", "amount": 200.00},
                {"id": uuid.uuid4(), "description": "Another expense", "date": "2023-12-03", "amount": -50.00}
            ]
        }
        
        response = self.client.post('/api/v1/enrichment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Calcula la tasa de categorización esperada
        categorization_rate_expected = 2 / 3 * 100  # 2 transacciones categorizadas / 3 transacciones totales * 100
        
        self.assertEqual(response.data['categorization_rate'], categorization_rate_expected)
