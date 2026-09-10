from rest_framework import serializers
from .models import Bid,BidDocument,BidItem
class BidItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=BidItem; fields="__all__"
class BidDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=BidDocument; fields=["id","bid","name","file","uploaded_at"]
        read_only_fields=["uploaded_at"]
class BidSerializer(serializers.ModelSerializer):
    items=BidItemSerializer(many=True,read_only=True)
    documents=BidDocumentSerializer(many=True,read_only=True)
    class Meta:
        model=Bid; fields=["id","tender","bidder","reference","total_amount","emd_reference","status","submitted_at","created_at","documents","items"]
        read_only_fields=["bidder","reference","status","submitted_at","created_at"]
