from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tender(models.Model):
    STATUS=[("DRAFT","Draft"),("OPEN","Open"),("CLOSED","Closed"),("EVALUATION","Evaluation"),("AWARDED","Awarded"),("CANCELLED","Cancelled")]
    tender_id=models.CharField(max_length=50,unique=True)
    title=models.CharField(max_length=255)
    category=models.CharField(max_length=100)
    location=models.CharField(max_length=255,blank=True)
    procurement_method=models.CharField(max_length=100,default="Open Tendering")
    description=models.TextField(blank=True)
    publication_date=models.DateTimeField(default=timezone.now)
    submission_deadline=models.DateTimeField()
    opening_date=models.DateTimeField()
    emd_type=models.CharField(max_length=50,blank=True)
    emd_amount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    financial_evaluation_percent=models.DecimalField(max_digits=5,decimal_places=2,default=100)
    status=models.CharField(max_length=20,choices=STATUS,default="DRAFT")
    created_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name="created_tenders")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def effective_status(self):
        if self.status=="OPEN" and timezone.now() >= self.submission_deadline:
            return "CLOSED"
        return self.status
    def save(self,*args,**kwargs):
        if self.status=="OPEN" and self.submission_deadline <= timezone.now():
            self.status="CLOSED"
        super().save(*args,**kwargs)
    def __str__(self): return f"{self.tender_id} - {self.title}"

class TenderItem(models.Model):
    tender=models.ForeignKey(Tender,on_delete=models.CASCADE,related_name="items")
    line_no=models.PositiveIntegerField(default=1)
    description=models.CharField(max_length=500)
    unit=models.CharField(max_length=50,blank=True)
    quantity=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    estimated_price=models.DecimalField(max_digits=14,decimal_places=2,default=0)

    class Meta:
        ordering=["line_no","id"]

    def __str__(self): return f"{self.tender.tender_id} - {self.line_no}"

class TenderDocument(models.Model):
    tender=models.ForeignKey(Tender,on_delete=models.CASCADE,related_name="documents")
    name=models.CharField(max_length=255)
    file=models.FileField(upload_to="tenders/%Y/%m/")
    uploaded_at=models.DateTimeField(auto_now_add=True)
