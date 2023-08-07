from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice

class InvoiceAPITestCase(APITestCase):
    def test_create_invoice(self):
        data = {
            'date': '2023-08-05',
            'invoice_no': 'INV-001',
            'customer_name': 'John Doe',
            'details': [
                {
                    'description': 'Product A',
                    'quantity': 2,
                    'unit_price': '10.00',
                    'price': '20.00'
                }
            ]
        }

        response = self.client.post('/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)

    def test_get_invoice(self):
        invoice = Invoice.objects.create(
            date='2023-08-05',
            invoice_no='INV-001',
            customer_name='John Doe'
        )

        response = self.client.get(f'/invoices/{invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
