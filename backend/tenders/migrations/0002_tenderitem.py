from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tenders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TenderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("line_no", models.PositiveIntegerField(default=1)),
                ("description", models.CharField(max_length=500)),
                ("unit", models.CharField(blank=True, max_length=50)),
                ("quantity", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("estimated_price", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("tender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="tenders.tender")),
            ],
            options={"ordering": ["line_no", "id"]},
        ),
    ]