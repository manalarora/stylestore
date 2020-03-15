# Generated by Django 3.0.4 on 2020-03-15 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(max_length=50)),
                ('line_2', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('pin_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6)),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_to', models.DateTimeField(auto_now_add=True)),
                ('discount_percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('gender', models.CharField(choices=[('f', 'Female'), ('m', 'Male'), ('u', 'Undisclosed')], max_length=1, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Styles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('image_model', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('unit_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField()),
                ('payment_type', models.CharField(choices=[('c', 'Cash on delivery'), ('d', 'Debit Card'), ('p', 'PayTM')], max_length=1)),
                ('payment_status', models.BooleanField()),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('expected_delivery', models.DateTimeField()),
                ('delivered_at', models.DateTimeField()),
                ('coupon_used', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='CompleteDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_image', models.URLField()),
                ('result_design', models.URLField()),
                ('styled_templates', models.TextField()),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Styles')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_purchased', models.BooleanField()),
                ('styled_template_url', models.URLField()),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('complete_design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.CompleteDesign')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Templates')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.CustomUser')),
            ],
        ),
    ]
