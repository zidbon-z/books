# Generated by Django 4.0.2 on 2022-02-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_book_isbn10_book_isbn13_book_selflink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
    ]
