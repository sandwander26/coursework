from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0007_order_final_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='final_sum',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
