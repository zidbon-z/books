# Generated by Django 4.0.2 on 2022-03-08 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_book_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='shelf',
            field=models.ForeignKey(blank=True, default=8, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='books', to='main.shelf'),
        ),
    ]
