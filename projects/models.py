from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from pypinyin import lazy_pinyin


class Project(models.Model):
    """ 定义项目信息 """

    code = models.CharField(verbose_name="项目代码", unique=True, max_length=50)
    name = models.CharField(verbose_name="项目名称", max_length=50)
    describe = models.CharField(verbose_name="描述信息", blank=True, max_length=500)
    built_in = models.DateTimeField(blank=True, null=True, verbose_name="项目启动时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return self.code


class Station(models.Model):
    """ 台站信息 """

    PREPARE = "prepare"
    MAP = "map"
    PROSPECT = "prospect"
    TEST = "test"
    ONLINE = "online"
    PAUSE = "pause"
    STOP = "stop"
    UNKNOWN = "unknown"

    STATUS_TYPE = (
        (PREPARE, "预备"),
        (MAP, "图堪"),
        (PROSPECT, "堪选"),
        (TEST, "仪器堪选"),
        (ONLINE, "上线"),
        (PAUSE, "暂停"),
        (STOP, "停止"),
        (UNKNOWN, "未知"),
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="stations",
        verbose_name="所属项目",
    )
    code = models.CharField(verbose_name="代码", unique=True, max_length=50)
    name = models.CharField(verbose_name="名称", max_length=50)
    pinyin_name = models.CharField(verbose_name="拼音名称", max_length=50, blank=True)
    latitude = models.DecimalField(
        verbose_name="纬度", null=True, max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        verbose_name="经度", null=True, max_digits=9, decimal_places=6
    )
    altitude = models.DecimalField(
        verbose_name="高程", null=True, max_digits=7, decimal_places=2
    )
    built_in = models.DateTimeField(blank=True, null=True, verbose_name="启用时间")
    destroyed_in = models.DateTimeField(blank=True, null=True, verbose_name="撤销时间")
    status = models.CharField(
        verbose_name="状态", choices=STATUS_TYPE, default=PREPARE, max_length=50
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "project",
            "code",
        )
        ordering = (
            "project",
            "code",
        )

    def __str__(self):
        return f"{self.project.code}-{self.code}"

    def save(self, *args, **kwargs):
        if not self.pinyin_name:
            self.pinyin_name = "".join([s.capitalize() for s in lazy_pinyin(self.name)])
        super().save(*args, **kwargs)


class Department(models.Model):
    """ 单位部门 """

    name = models.CharField(verbose_name="部门名称", max_length=50)
    address = models.CharField(verbose_name="地址", blank=True, max_length=200)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class GeneralEquipmentCategory(models.Model):
    """ 设备仪器分类 """

    name = models.CharField(verbose_name="分类名称", unique=True, max_length=50)
    describe = models.CharField(verbose_name="分类描述", max_length=50)
    parent = models.ForeignKey(
        "self",
        verbose_name="上级分类",
        limit_choices_to={"parent__isnull": True},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )


class Equipment(models.Model):
    """ 设备仪器型号通用字段 """

    name = models.CharField(verbose_name="设备名称", max_length=100)
    brand = models.CharField(verbose_name="品牌", blank=True, max_length=50)
    manufacturer = models.CharField(verbose_name="厂商", blank=True, max_length=50)
    param = models.CharField(verbose_name="参数描述", blank=True, max_length=200)
    total = models.PositiveIntegerField(verbose_name="总数", default=0)

    class Meta:
        abstract = True

    def __str__(self):
        if self.param == "":
            return self.name
        else:
            return f"{self.name}({self.param})"


class GeneralEquipment(Equipment):
    """ 通用设备 """

    category = models.ForeignKey(
        GeneralEquipmentCategory, on_delete=models.CASCADE, related_name="equipments"
    )


class SeismicEquipmentModel(Equipment):
    """ 地震仪模型 """

    response_file = models.FileField(
        upload_to="upload_response_file", blank=True, null=True, verbose_name="仪器响应文件"
    )


class DataCollectorModel(Equipment):
    """ 数据采集器模型 """

    response_file = models.FileField(
        upload_to="upload_response_file", blank=True, null=True, verbose_name="仪器响应文件"
    )


class ProfessionalInstrumentEntity(models.Model):
    """ 设备实体 """

    ONLINE = "online"
    MALFUNCTION = "malfunction"
    WAREHOUSE = "warehouse"
    CHECK = "check"
    RETURNED = "returned"
    UNKNOWN = "unknown"
    STATUS_TYPE = (
        (ONLINE, "上线"),
        (MALFUNCTION, "故障"),
        (WAREHOUSE, "库存"),
        (CHECK, "待检测"),
        (RETURNED, "已归还"),
        (UNKNOWN, "未知"),
    )

    sn = models.CharField(verbose_name="设备序列号", max_length=50)
    status = models.CharField(verbose_name="状态", choices=STATUS_TYPE, max_length=50)
    belong = models.ForeignKey(
        "Department", verbose_name="所属单位", null=True, on_delete=models.SET_NULL
    )
    by_used = models.ForeignKey(
        "Station",
        verbose_name="那个台站在用",
        related_name="+",
        null=True,
        on_delete=models.SET_NULL,
    )
    get_in = models.DateTimeField(verbose_name="获得时间", null=True)
    lost_at = models.DateTimeField(verbose_name="失去时间", null=True)

    class Meta:
        abstract = True


class SeismicEquipmentEntity(ProfessionalInstrumentEntity):
    """ 地震仪实体 """

    model = models.ForeignKey(
        "SeismicEquipmentModel",
        on_delete=models.SET_NULL,
        null=True,
        related_name="entities",
    )

    def __str__(self):
        return f"{self.sn}-[{self.model}]"


class DataCollectorEntity(ProfessionalInstrumentEntity):
    """ 地震仪实体 """

    model = models.ForeignKey(
        "DataCollectorModel",
        on_delete=models.SET_NULL,
        null=True,
        related_name="entities",
    )

    def __str__(self):
        return f"{self.sn}-[{self.model}]"


class StationHistory(models.Model):
    """ 台站维护历史 """

    station = models.ForeignKey(
        "Station",
        on_delete=models.CASCADE,
        related_name="histories",
        unique_for_date="history_at",
    )
    history_at = models.DateTimeField()
    description = models.TextField(blank=True, verbose_name="描述信息")
    is_last = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.station} - {self.history_at}"


class Record(models.Model):
    history = models.ForeignKey(
        "StationHistory", on_delete=models.CASCADE, related_name="records"
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "ChangedLocationItem",
                "ChangedSeismicInstrumentEntitiesCombinationItem",
            )
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")


class BaseRecordItem(models.Model):
    """ 维护记录公共属性 """

    station = models.ForeignKey(
        "Station", on_delete=models.CASCADE, related_name="%(class)s_related"
    )
    happened_at = models.DateTimeField(verbose_name="发生时间")
    is_last = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("happened_at",)
        abstract = True


class ChangedLocationItem(BaseRecordItem):
    """ 台站位置变更记录 """

    latitude = models.DecimalField(
        verbose_name="纬度", null=True, max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        verbose_name="经度", null=True, max_digits=9, decimal_places=6
    )
    altitude = models.DecimalField(
        verbose_name="高程", null=True, max_digits=7, decimal_places=2
    )
    is_real = models.BooleanField(default=False, verbose_name="是否是真实位置(实堪)")


class ChangedSeismicInstrumentEntitiesCombinationItem(BaseRecordItem):
    collector = models.ForeignKey(
        "DataCollectorEntity",
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
    )
    seismograph = models.ForeignKey(
        "SeismicEquipmentEntity",
        on_delete=models.SET_NULL,
        null=True,
        related_name="items",
    )
