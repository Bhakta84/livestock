from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("bids", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="BidderProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("vendor_name", models.CharField(max_length=255)),
                ("vendor_type", models.CharField(max_length=100)),
                ("tpn_number", models.CharField(max_length=100)),
                ("license_no", models.CharField(max_length=100)),
                ("trade_license", models.FileField(upload_to="bidder-registrations/%Y/%m/")),
                ("address_details", models.TextField()),
                ("contact_details", models.CharField(max_length=255)),
                ("terms_accepted", models.BooleanField(default=False)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="bidder_profile", to="auth.user")),
            ],
        ),
    ]