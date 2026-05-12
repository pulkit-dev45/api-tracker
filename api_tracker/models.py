from django.db import models
from django.contrib.auth.models import User

class ApiLog(models.Model):
    METHOD_TYPE=[
        ("GET","GET"),
        ("POST","POST"),
        ("PUT","PUT"),
        ("PATCH","PATCH"),
        ("DELETE","DELETE")
    ]
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    endPoint=models.CharField(max_length=200)
    ipAddress=models.GenericIPAddressField(null=True,blank=True)
    statusCode=models.IntegerField()
    methodType=models.CharField(choices=METHOD_TYPE)
    responseTime=models.FloatField()
    timeStamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.endPoint}-{self.statusCode}-{self.methodType}-{self.responseTime}-{self.timeStamp}"
