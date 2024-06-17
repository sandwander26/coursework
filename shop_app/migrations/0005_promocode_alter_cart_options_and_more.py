from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0004_flowerlist_archived_flowerlist_number_of_uses_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10)),
                ('count', models.SmallIntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='cart',
            options={},
        ),
        migrations.AlterModelOptions(
            name='flowerlist',
            options={},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
    ]
