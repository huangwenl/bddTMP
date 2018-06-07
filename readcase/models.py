from django.db import models


# # Create your models here.

class testcase(models.Model):
    __table__ = 'case'
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField(null=False, default=0)
    title = models.CharField(max_length=100)  # 模块名称
    isAction = models.BooleanField(default=False)  # 是否已执行0,1
    result = models.IntegerField(null=True)  # 执行结果(0success,1fail,2skip)
    user = models.CharField(max_length=20, null=True)  # 执行人
    create_time = models.DateTimeField(auto_now=True)  # 创建时间

    def __str__(self):
        return self.title


class case(models.Model):
    project = models.CharField(max_length=50)
    caseId = models.IntegerField(null=False, default=0)
    modelName = models.CharField(max_length=50)
    caseDetail = models.CharField(max_length=100)
    isAction = models.BooleanField(default=False)  # 是否已执行0,1
    result = models.IntegerField(null=True)  # 执行结果(0success,1fail,2skip)
    user = models.CharField(max_length=20, null=True)  # 执行人
    action_time = models.DateTimeField(auto_now=True)  # 执行时间

    def __str__(self):
        return '%s %s %s' % (self.project, self.modelName, self.caseDetail)

    class Meta:
        unique_together = ("id", "caseId")
