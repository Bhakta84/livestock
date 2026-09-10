from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Tender, TenderDocument, TenderItem
from .serializers import TenderSerializer, TenderDocumentSerializer, TenderItemSerializer
from .permissions import StaffTenderPermission

class TenderViewSet(viewsets.ModelViewSet):
    queryset=Tender.objects.all().order_by("-created_at")
    serializer_class=TenderSerializer
    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [permissions.IsAuthenticated()]
        return [StaffTenderPermission()]
    def perform_create(self,serializer):
        try:
            serializer.save(created_by=self.request.user)
        except IntegrityError:
            raise ValidationError({"tender_id": "A tender with this ID already exists."})
    @action(detail=True,methods=["post"],permission_classes=[StaffTenderPermission])
    def publish(self,request,pk=None):
        tender=self.get_object()
        if tender.submission_deadline <= timezone.now():
            return Response({"detail":"Submission deadline must be in the future."},status=400)
        tender.status="OPEN"; tender.save(update_fields=["status","updated_at"])
        return Response(TenderSerializer(tender).data)
    @action(detail=True,methods=["post"],permission_classes=[StaffTenderPermission])
    def close(self,request,pk=None):
        tender=self.get_object(); tender.status="CLOSED"; tender.save()
        return Response(TenderSerializer(tender).data)

class TenderDocumentViewSet(viewsets.ModelViewSet):
    queryset=TenderDocument.objects.all().order_by("-uploaded_at")
    serializer_class=TenderDocumentSerializer
    parser_classes=[MultiPartParser,FormParser]
    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [permissions.IsAuthenticated()]
        return [StaffTenderPermission()]

class TenderItemViewSet(viewsets.ModelViewSet):
    queryset=TenderItem.objects.all()
    serializer_class=TenderItemSerializer
    permission_classes=[StaffTenderPermission]
