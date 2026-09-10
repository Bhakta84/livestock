from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tenders.models import Tender

class BidderProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="bidder_profile")
    vendor_name=models.CharField(max_length=255)
    vendor_type=models.CharField(max_length=100)
    tpn_number=models.CharField(max_length=100)
    license_no=models.CharField(max_length=100)
    trade_license=models.FileField(upload_to="bidder-registrations/%Y/%m/")
    address_details=models.TextField()
    contact_details=models.CharField(max_length=255)
    terms_accepted=models.BooleanField(default=False)
    submitted_at=models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.vendor_name

class Bid(models.Model):
    STATUS=[("DRAFT","Draft"),("SUBMITTED","Submitted"),("WITHDRAWN","Withdrawn")]
    tender=models.ForeignKey(Tender,on_delete=models.PROTECT,related_name="bids")
    bidder=models.ForeignKey(User,on_delete=models.PROTECT,related_name="bids")
    reference=models.CharField(max_length=60,unique=True)
    total_amount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    emd_reference=models.CharField(max_length=100,blank=True)
    status=models.CharField(max_length=20,choices=STATUS,default="DRAFT")
    submitted_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=("tender","bidder")
    def submit(self):
        if self.tender.effective_status()!="OPEN":
            raise ValueError("Tender is closed; bid submission is disabled.")
        self.status="SUBMITTED"; self.submitted_at=timezone.now(); self.save()
    def __str__(self): return self.reference

class BidDocument(models.Model):
    bid=models.ForeignKey(Bid,on_delete=models.CASCADE,related_name="documents")
    name=models.CharField(max_length=255)
    file=models.FileField(upload_to="bids/%Y/%m/")
    uploaded_at=models.DateTimeField(auto_now_add=True)
