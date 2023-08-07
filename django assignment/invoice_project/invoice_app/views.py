# from django.shortcuts import render

# Create your views here.
# from rest_framework import viewsets
# from .models import Invoice
# from .serializers import InvoiceSerializer

# class InvoiceViewSet(viewsets.ModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceSerializer

# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer,InvoiceDetailSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def perform_create(self, serializer):
        # Extract the details data from the request
        details_data = self.request.data.get('details', [])

        # Create the Invoice object first
        invoice = serializer.save()

        # Create associated InvoiceDetail objects
        for detail_data in details_data:
            detail_data['invoice'] = invoice.id
            detail_serializer = InvoiceDetailSerializer(data=detail_data)
            detail_serializer.is_valid(raise_exception=True)
            detail_serializer.save()

    def perform_update(self, serializer):
        # Extract the details data from the request
        details_data = self.request.data.get('details', [])

        # Save the updated Invoice object
        invoice = serializer.save()

        # Create or update associated InvoiceDetail objects
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                # If detail_id is provided, update the existing detail object
                detail_instance = InvoiceDetail.objects.get(id=detail_id, invoice=invoice)
                detail_serializer = InvoiceDetailSerializer(
                    instance=detail_instance, data=detail_data, partial=True
                )
            else:
                # If detail_id is not provided, create a new detail object
                detail_data['invoice'] = invoice.id
                detail_serializer = InvoiceDetailSerializer(data=detail_data)

            detail_serializer.is_valid(raise_exception=True)
            detail_serializer.save()
