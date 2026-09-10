from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from django.utils import timezone
from datetime import timedelta
from tenders.models import Tender
class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        u,_=User.objects.get_or_create(username="admin",defaults={"is_staff":True,"is_superuser":True})
        u.is_staff=True; u.is_superuser=True; u.set_password("Admin@12345"); u.save()
        for name in ["Admin","Procurement Officer","Evaluator","Approving Authority","Bidder"]:
            Group.objects.get_or_create(name=name)
        Tender.objects.get_or_create(
            tender_id="BLDCL/2026/001",
            defaults=dict(title="Supply of Animal Feed",category="Goods",location="BLDCL",
            procurement_method="Open Tendering",description="Demo tender for development testing.",
            publication_date=timezone.now(),submission_deadline=timezone.now()+timedelta(days=20),
            opening_date=timezone.now()+timedelta(days=20,hours=2),emd_type="Lumpsum",
            emd_amount=6000,financial_evaluation_percent=100,status="OPEN",created_by=u))
        self.stdout.write(self.style.SUCCESS("Demo data created. admin / Admin@12345"))
