from djongo import models


class Organization(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='organization')
    youdu_id = models.IntegerField(verbose_name='有度ID', null=True)
    level = models.IntegerField(verbose_name='部门等级', default=1)

    class Meta:
        db_table = "users_organization"


class UsersModel(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    nickname = models.CharField(max_length=32, verbose_name='花名')
    name = models.CharField(max_length=32, verbose_name='真名', default='')
    email = models.CharField(max_length=128, verbose_name='邮箱', null=True)
    phone = models.CharField(max_length=18, verbose_name='电话', null=True)
    sex = models.IntegerField(verbose_name='性别', default=1)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_set')

    class Meta:
        db_table = "users_user"
