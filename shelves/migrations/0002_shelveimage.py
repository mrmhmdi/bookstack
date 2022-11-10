# Generated by Django 4.1.3 on 2022-11-09 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shelves', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='shelveImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='media/images/default.jpg', upload_to='media/images/shelves')),
                ('shelve', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shelves.shelve')),
            ],
        ),
    ]
