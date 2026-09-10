from rest_framework import serializers
from .models import Tender, TenderDocument, TenderItem
class TenderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=TenderItem
        fields="__all__"

class TenderDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=TenderDocument
        fields=["id","name","file","uploaded_at"]
class TenderSerializer(serializers.ModelSerializer):
    items=TenderItemSerializer(many=True,read_only=True)
    documents=TenderDocumentSerializer(many=True,read_only=True)
    status=serializers.SerializerMethodField()
    class Meta:
        model=Tender
        fields="__all__"
        read_only_fields=["created_by","created_at","updated_at"]
    def get_status(self,obj): return obj.effective_status()
