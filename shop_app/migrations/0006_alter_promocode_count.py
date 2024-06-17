import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0005_promocode_alter_cart_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='count',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
