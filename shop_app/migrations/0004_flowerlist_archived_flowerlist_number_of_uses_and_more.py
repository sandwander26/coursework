from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0003_rename_flowerslist_flowerlist_alter_cart_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowerlist',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='flowerlist',
            name='number_of_uses',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='flowerlist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='flowers/'),
        ),
    ]
