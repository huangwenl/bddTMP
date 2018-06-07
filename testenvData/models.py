from django.db import models


# Create your models here.
class envdata(models.Model):
    env = models.CharField(max_length=50, null=True)
    channle = models.CharField(max_length=10, null=True)
    role = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=15, null=True)
    password = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.phone

    class Meta:
        unique_together = ("id", "phone")


class serverdata(models.Model):
    env = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=50, null=True)
    port = models.IntegerField(null=True)
    user = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    isAvailable = models.CharField(max_length=4, null=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip

    def setattr(self, key, value):
        self.__setattr__(key, value)


class mobileInfo(models.Model):
    brand = models.CharField(max_length=20, null=False)
    type = models.CharField(max_length=30, null=False)
    equip = models.CharField(max_length=50, null=False)
    os = models.CharField(max_length=50, null=False)
    person = models.CharField(max_length=20, null=False)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type
