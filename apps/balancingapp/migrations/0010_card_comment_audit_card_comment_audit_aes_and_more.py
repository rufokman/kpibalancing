# Generated by Django 4.1.2 on 2022-10-20 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balancingapp', '0009_card_kpi_kls2'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='comment_audit',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='comment_audit_AES',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='comment_func',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='fact',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='passport',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='verificator',
            field=models.TextField(null=True),
        ),
    ]