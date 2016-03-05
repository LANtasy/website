# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('salesbro', '0005_auto_20151024_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('payment_type', models.CharField(max_length=10, verbose_name='Payment type', choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('discover', 'Discover'), ('amex', 'American Express'), ('debit', 'Debit'), ('cash', 'Cash')])),
                ('phone', models.CharField(max_length=20)),
                ('key', models.CharField(max_length=255)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
        ),
    ]
