# Generated by Django 2.2.14 on 2020-07-24 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCollectorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='设备名称')),
                ('brand', models.CharField(blank=True, max_length=50, verbose_name='品牌')),
                ('manufacturer', models.CharField(blank=True, max_length=50, verbose_name='厂商')),
                ('param', models.CharField(blank=True, max_length=200, verbose_name='参数描述')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('response_file', models.FileField(blank=True, null=True, upload_to='upload_response_file', verbose_name='仪器响应文件')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='部门名称')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='地址')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='项目代码')),
                ('name', models.CharField(max_length=50, verbose_name='项目名称')),
                ('describe', models.CharField(blank=True, max_length=500, verbose_name='描述信息')),
                ('built_in', models.DateTimeField(blank=True, null=True, verbose_name='项目启动时间')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='SeismicEquipmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='设备名称')),
                ('brand', models.CharField(blank=True, max_length=50, verbose_name='品牌')),
                ('manufacturer', models.CharField(blank=True, max_length=50, verbose_name='厂商')),
                ('param', models.CharField(blank=True, max_length=200, verbose_name='参数描述')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('response_file', models.FileField(blank=True, null=True, upload_to='upload_response_file', verbose_name='仪器响应文件')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='代码')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('pinyin_name', models.CharField(blank=True, max_length=50, verbose_name='拼音名称')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='纬度')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='经度')),
                ('altitude', models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='高程')),
                ('built_in', models.DateTimeField(blank=True, null=True, verbose_name='启用时间')),
                ('destroyed_in', models.DateTimeField(blank=True, null=True, verbose_name='撤销时间')),
                ('status', models.CharField(choices=[('prepare', '预备'), ('map', '图堪'), ('prospect', '堪选'), ('test', '仪器堪选'), ('online', '上线'), ('pause', '暂停'), ('stop', '停止'), ('unknown', '未知')], default='prepare', max_length=50, verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stations', to='projects.Project', verbose_name='所属项目')),
            ],
            options={
                'ordering': ('project', 'code'),
                'unique_together': {('project', 'code')},
            },
        ),
        migrations.CreateModel(
            name='StationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_at', models.DateTimeField()),
                ('description', models.TextField(blank=True, verbose_name='描述信息')),
                ('is_last', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='histories', to='projects.Station', unique_for_date='history_at')),
            ],
        ),
        migrations.CreateModel(
            name='SeismicEquipmentEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=50, verbose_name='设备序列号')),
                ('status', models.CharField(choices=[('online', '上线'), ('malfunction', '故障'), ('warehouse', '库存'), ('check', '待检测'), ('returned', '已归还'), ('unknown', '未知')], max_length=50, verbose_name='状态')),
                ('get_in', models.DateTimeField(null=True, verbose_name='获得时间')),
                ('lost_at', models.DateTimeField(null=True, verbose_name='失去时间')),
                ('belong', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.Department', verbose_name='所属单位')),
                ('by_used', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.Station', verbose_name='那个台站在用')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entities', to='projects.SeismicEquipmentModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('ChangedLocationItem', 'ChangedSeismicInstrumentEntitiesCombinationItem')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='projects.StationHistory')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralEquipmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='分类名称')),
                ('describe', models.CharField(max_length=50, verbose_name='分类描述')),
                ('parent', models.ForeignKey(blank=True, limit_choices_to={'parent__isnull': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='projects.GeneralEquipmentCategory', verbose_name='上级分类')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='设备名称')),
                ('brand', models.CharField(blank=True, max_length=50, verbose_name='品牌')),
                ('manufacturer', models.CharField(blank=True, max_length=50, verbose_name='厂商')),
                ('param', models.CharField(blank=True, max_length=200, verbose_name='参数描述')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='总数')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='projects.GeneralEquipmentCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataCollectorEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn', models.CharField(max_length=50, verbose_name='设备序列号')),
                ('status', models.CharField(choices=[('online', '上线'), ('malfunction', '故障'), ('warehouse', '库存'), ('check', '待检测'), ('returned', '已归还'), ('unknown', '未知')], max_length=50, verbose_name='状态')),
                ('get_in', models.DateTimeField(null=True, verbose_name='获得时间')),
                ('lost_at', models.DateTimeField(null=True, verbose_name='失去时间')),
                ('belong', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.Department', verbose_name='所属单位')),
                ('by_used', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='projects.Station', verbose_name='那个台站在用')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entities', to='projects.DataCollectorModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChangedSeismicInstrumentEntitiesCombinationItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happened_at', models.DateTimeField(verbose_name='发生时间')),
                ('is_last', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='projects.DataCollectorEntity')),
                ('seismograph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='projects.SeismicEquipmentEntity')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changedseismicinstrumententitiescombinationitem_related', to='projects.Station')),
            ],
            options={
                'ordering': ('happened_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChangedLocationItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happened_at', models.DateTimeField(verbose_name='发生时间')),
                ('is_last', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='纬度')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='经度')),
                ('altitude', models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='高程')),
                ('is_real', models.BooleanField(default=False, verbose_name='是否是真实位置(实堪)')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changedlocationitem_related', to='projects.Station')),
            ],
            options={
                'ordering': ('happened_at',),
                'abstract': False,
            },
        ),
    ]
