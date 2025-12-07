from django.db import models
from apps.oaauth.models import OAUser, OADepartment


# 通知相关模型
class Inform(models.Model):
    # 通知标题
    title = models.CharField(max_length=100)
    # 通知内容
    content = models.TextField()
    # 通知创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 通知是否公开,有些通知一些人能看,有些通知所有人能看
    # 如果前端上传的department_ids中包含了0，比如[0]，那么就认为这个通知是所有部门可见,public设置为true
    public = models.BooleanField(default=False)
    # 通知是由谁发布的
    author = models.ForeignKey(OAUser, on_delete=models.CASCADE, related_name='informs', related_query_name='informs')
    # 通知哪些部门可见,多对多关系
    departments = models.ManyToManyField(OADepartment, related_name='informs', related_query_name='informs')

    class Meta:
        # 以通知创建时间倒序排序
        ordering = ('-create_time',)

# 记录谁读过通知
class InformRead(models.Model):
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, related_name='reads', related_query_name='reads')
    user = models.ForeignKey(OAUser, on_delete=models.CASCADE, related_name='reads', related_query_name='reads')
    read_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # inform和user组合的数据，必须是唯一的,谁读过通知,数据库中只能有一条数据
        unique_together = ('inform', 'user')
