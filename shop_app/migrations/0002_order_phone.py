from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
