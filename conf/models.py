from django.db import models as m


class Setting(m.Model):
    key = m.CharField(max_length=255, unique=True)
    value = m.CharField(max_length=1000)
    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)
