import secrets
from rest_framework import viewsets,permissions
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bid,BidDocument,BidItem
from .serializers import BidSerializer,BidDocumentSerializer,BidItemSerializer

class BidViewSet(viewsets.ModelViewSet):
    serializer_class=BidSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Bid.objects.all().order_by("-created_at")
        return Bid.objects.filter(bidder=self.request.user).order_by("-created_at")
    def perform_create(self,serializer):
        tender=serializer.validated_data["tender"]
        if tender.effective_status()!="OPEN":
            raise ValidationError("Tender is closed; bids cannot be created.")
        existing=Bid.objects.filter(tender=tender,bidder=self.request.user).first()
        if existing:
            raise ValidationError({"detail": "You already have a bid for this tender.", "bid_id": existing.id})
        ref=f"BID-{tender.tender_id.replace('/','-')}-{secrets.token_hex(4).upper()}"
        try:
            serializer.save(bidder=self.request.user,reference=ref)
        except IntegrityError:
            raise ValidationError("You already have a bid for this tender.")
    @action(detail=True,methods=["post"])
    def submit(self,request,pk=None):
        bid=self.get_object()
        if bid.bidder != request.user and not request.user.is_staff:
            return Response({"detail":"Not permitted."},status=403)
        try: bid.submit()
        except ValueError as e: return Response({"detail":str(e)},status=400)
        return Response(BidSerializer(bid).data)
    @action(detail=True,methods=["post"],url_path="items")
    def save_items(self,request,pk=None):
        bid=self.get_object()
        if bid.bidder != request.user and not request.user.is_staff:
            return Response({"detail":"Not permitted."},status=403)
        if bid.status!="DRAFT":
            return Response({"detail":"Only draft bids can be edited."},status=400)
        items=request.data.get("items",[])
        bid.items.all().delete()
        for index,item in enumerate(items,1):
            tender_item_id=item.get("boq_item_id")
            tender_item=bid.tender.items.filter(id=tender_item_id).first() if tender_item_id else None
            quantity=item.get("quantity", tender_item.quantity if tender_item else 0)
            rate=item.get("rate",0)
            BidItem.objects.create(bid=bid,tender_item=tender_item,line_no=index,description=item.get("description",tender_item.description if tender_item else ""),unit=item.get("unit",tender_item.unit if tender_item else ""),quantity=quantity,rate=rate,amount=item.get("amount",0))
        total=sum(item.amount for item in bid.items.all())
        bid.total_amount=total; bid.save(update_fields=["total_amount"])
        return Response(BidSerializer(bid).data)

class BidDocumentViewSet(viewsets.ModelViewSet):
    serializer_class=BidDocumentSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return BidDocument.objects.filter(bid__bidder=self.request.user) if not self.request.user.is_staff else BidDocument.objects.all()
