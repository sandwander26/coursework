from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0006_alter_promocode_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='final_sum',
            field=models.SmallIntegerField(default=2500),
            preserve_default=False,
        ),
    ]
