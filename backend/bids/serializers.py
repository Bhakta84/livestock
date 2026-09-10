from rest_framework import serializers
from .models import Bid,BidDocument
class BidDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=BidDocument; fields=["id","name","file","uploaded_at"]
class BidSerializer(serializers.ModelSerializer):
    documents=BidDocumentSerializer(many=True,read_only=True)
    class Meta:
        model=Bid; fields=["id","tender","bidder","reference","total_amount","emd_reference","status","submitted_at","created_at","documents"]
        read_only_fields=["bidder","reference","status","submitted_at","created_at"]
