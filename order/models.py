from datetime import datetime

from django.db import models

from utils.common import CommonFields


class OrderFormModel(CommonFields):
    name = models.CharField(max_length=32, verbose_name="名称", unique=True)
    label = models.CharField(max_length=32, verbose_name="别名")
    type = models.CharField(max_length=32, verbose_name="表单字段类型", default="input")
    sort = models.IntegerField(verbose_name="排序", default=1)
    options = models.JSONField(verbose_name="字段可选项", default=dict)

    class Meta:
        db_table = "order_form"


class OrderApprovalModel(CommonFields):
    name = models.CharField(max_length=32, verbose_name="名称", unique=True)
    label = models.CharField(max_length=32, verbose_name="别名")
    sort = models.IntegerField(verbose_name="排序", default=1)
    options = models.JSONField(verbose_name="字段可选项", default=dict)

    class Meta:
        db_table = "order_approval"


class OrderTemplateModel(CommonFields):
    name = models.CharField(max_length=32, verbose_name="名称", unique=True)
    code = models.CharField(max_length=32, verbose_name="英文标识")
    resource_type = models.CharField(
        max_length=32, verbose_name="工单资源类型", choices=[]
    )
    icon = models.CharField(max_length=32, verbose_name="图标")
    form = models.ForeignKey(
        OrderFormModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="form_set",
        verbose_name="工单表单",
    )
    form = models.ForeignKey(
        OrderApprovalModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="form_set",
        verbose_name="工单审批流",
    )
    desc = models.CharField(max_length=255, verbose_name="描述", default="")

    class Meta:
        db_table = "order_template"


class OrderInstaceModel(CommonFields):
    title = models.CharField(max_length=32, verbose_name="主题")
    serial = models.CharField(max_length=32, verbose_name="序列号", unique=True)
    order_code = models.CharField(max_length=32, verbose_name="工单标识")
    order_type = models.CharField(max_length=32, verbose_name="工单类型")
    order_status = models.CharField(max_length=32, verbose_name="工单状态", choices=[])
    currrent_node = models.CharField(max_length=32, verbose_name="当前节点")
    description = models.CharField(
        max_length=255, verbose_name="业务线描述", default=""
    )

    class Meta:
        db_table = "order_instance"


class OrderInstaceFormModel(models.Model):
    instance_form = models.ForeignKey(
        OrderInstaceModel,
        on_delete=models.CASCADE,
        related_name="instance_form",
        verbose_name="工单实例",
    )
    name = models.CharField(max_length=32, verbose_name="字段名称")
    label = models.CharField(max_length=32, verbose_name="字段别名")
    value = models.TextField(verbose_name="字段值")
    type = models.CharField(max_length=32, verbose_name="字段类型")
    sort = models.CharField(max_length=32, verbose_name="字段排序")
    options = models.JSONField(verbose_name="字段可选项", default=dict)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "order_instance_form"


class OrderInstaceApprovalModel(CommonFields):
    instance_apprval = models.ForeignKey(
        OrderInstaceModel,
        on_delete=models.CASCADE,
        related_name="instance_approval",
        verbose_name="工单实例",
    )
    name = models.CharField(max_length=32, verbose_name="字段名称")
    label = models.CharField(max_length=32, verbose_name="字段别名")
    approval_users = models.JSONField(verbose_name="可审批人员", default=list)
    approval_user = models.JSONField(verbose_name="审批人员", default=dict)
    approval_context = models.TextField(verbose_name="审批内容", default="")
    approval_at = models.DateTimeField(verbose_name="审批时间", default=datetime.now)
    sort = models.CharField(max_length=32, verbose_name="字段排序")
    options = models.JSONField(verbose_name="字段可选项", default=dict)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "order_instance_approval"


class OrderApprovalStatusModel(models.Model):
    order_status = models.ForeignKey(OrderInstaceModel, on_delete=models.CASCADE)
    approval_status = models.ForeignKey(OrderInstaceApprovalModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, verbose_name="审批类型", choices=[])
    userid= models.CharField(max_length=32, verbose_name="用户ID")
    username = models.CharField(max_length=32, verbose_name="用户名")
    nickname = models.CharField(max_length=32, verbose_name="别名")
    is_approval = models.BooleanField(verbose_name="是否审批", default=False)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "order_approval_status"


class OrderApprovalItemsModel(models.Model):
    order_items = models.ForeignKey(OrderInstaceModel, on_delete=models.CASCADE)
    approval_items = models.ForeignKey(OrderInstaceApprovalModel, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, verbose_name="审批类型", choices=[])
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    from_user = models.JSONField(verbose_name="原审批人员", default=dict)
    to_user = models.JSONField(verbose_name="目标审批人员", default=dict)
    create_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "order_approval_items"
