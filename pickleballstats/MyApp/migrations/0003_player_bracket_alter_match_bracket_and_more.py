# Generated by Django 5.0.2 on 2024-02-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_rename_counter_loser_count_playerstats_counter_losers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='bracket',
            field=models.CharField(choices=[('MS', 'Mens Singles'), ('WS', "Women's Singles")], default='MS', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='match',
            name='bracket',
            field=models.CharField(choices=[('MS', "Men's Singles"), ('MD', "Men's Doubles"), ('MXD', 'Mixed Doubles'), ('WD', "Women's Doubles"), ('WS', "Women's Singles")], max_length=3),
        ),
        migrations.AlterField(
            model_name='team',
            name='bracket',
            field=models.CharField(choices=[('MD', "Men's Doubles"), ('MXD', 'Mixed Doubles'), ('WD', "Women's Doubles")], max_length=3),
        ),
    ]