from django.db import models


class CommonFields(models.Model):
    """
    公共字段
    """

    id = models.AutoField(primary_key=True)
    create_by = models.CharField(max_length=64, verbose_name="创建人", default="")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True
