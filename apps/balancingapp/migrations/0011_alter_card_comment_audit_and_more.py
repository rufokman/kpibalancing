# Generated by Django 4.1.2 on 2022-10-20 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balancingapp', '0010_card_comment_audit_card_comment_audit_aes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='comment_audit',
            field=models.TextField(null=True, verbose_name='Комментарии по аудиту (заполняется СУП УК)'),
        ),
        migrations.AlterField(
            model_name='card',
            name='comment_audit_AES',
            field=models.TextField(null=True, verbose_name='Комментарии по аудиту (заполняется сотрудником АЭС/ДО)'),
        ),
        migrations.AlterField(
            model_name='card',
            name='comment_func',
            field=models.TextField(null=True, verbose_name='Комментарий от функции (по необходимости)'),
        ),
        migrations.AlterField(
            model_name='card',
            name='fact',
            field=models.TextField(null=True, verbose_name='Факт выполнения'),
        ),
        migrations.AlterField(
            model_name='card',
            name='fio',
            field=models.CharField(max_length=300, verbose_name='ФИО сотрудника, в чью карту устанавливается КПЭ'),
        ),
        migrations.AlterField(
            model_name='card',
            name='id_kpi',
            field=models.PositiveIntegerField(null=True, verbose_name='ID КПЭ в ИС РЕКОРД'),
        ),
        migrations.AlterField(
            model_name='card',
            name='kpi_kls2',
            field=models.TextField(null=True, verbose_name='КПЭ / КлС2'),
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=3000, verbose_name='Наименование КПЭ / КлС'),
        ),
        migrations.AlterField(
            model_name='card',
            name='passport',
            field=models.TextField(null=True, verbose_name='Паспорт'),
        ),
        migrations.AlterField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Последнее обновление'),
        ),
        migrations.AlterField(
            model_name='card',
            name='verificator',
            field=models.TextField(null=True, verbose_name='Инициатор / Верификатор'),
        ),
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('name_col', models.TextField()),
                ('id_kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balancingapp.card')),
            ],
            options={
                'db_table': 'change',
                'managed': True,
            },
        ),
    ]