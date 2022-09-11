# Generated by Django 4.1 on 2022-09-11 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="user",
            name="currency",
            field=models.CharField(
                choices=[("krw", "Korean ₩"), ("usd", "Dollar $")],
                default="krw",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female")],
                default="male",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[("kr", "Korean"), ("en", "English")],
                default="kr",
                max_length=2,
            ),
        ),
    ]
