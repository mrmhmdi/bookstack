# Generated by Django 4.1.3 on 2022-12-07 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstack', '0002_page_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagereview',
            name='page',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='bookstack.page'),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='authors', to=settings.AUTH_USER_MODEL),
        ),
    ]
