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
    tender_reference=serializers.CharField(source="tender.tender_id",read_only=True)
    bidder_name=serializers.SerializerMethodField()
    class Meta:
        model=Bid; fields=["id","tender","tender_reference","bidder","bidder_name","reference","total_amount","emd_reference","status","submitted_at","created_at","documents","items"]
        read_only_fields=["bidder","reference","status","submitted_at","created_at"]

    def get_bidder_name(self,obj):
        profile=getattr(obj.bidder,"bidder_profile",None)
        return profile.vendor_name if profile else (obj.bidder.get_full_name() or obj.bidder.username)
