from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0002_order_phone'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FlowersList',
            new_name='FlowerList',
        ),
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='flowerlist',
            options={'ordering': ['pk'], 'verbose_name_plural': 'Flowers'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'orders'},
        ),
    ]
