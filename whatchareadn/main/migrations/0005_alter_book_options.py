# Generated by Django 4.0.2 on 2022-02-17 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_book_owned_book_reading'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
    ]