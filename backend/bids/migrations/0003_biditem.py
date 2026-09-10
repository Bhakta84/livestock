from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("bids", "0002_bidderprofile"), ("tenders", "0002_tenderitem")]

    operations = [
        migrations.CreateModel(
            name="BidItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("line_no", models.PositiveIntegerField(default=1)),
                ("description", models.CharField(max_length=500)),
                ("unit", models.CharField(blank=True, max_length=50)),
                ("quantity", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("rate", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("bid", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="bids.bid")),
                ("tender_item", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="bid_items", to="tenders.tenderitem")),
            ],
            options={"ordering": ["line_no", "id"]},
        ),
    ]