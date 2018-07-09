from django.utils.translation import gettext as _
from django.contrib.auth.models import User, Group as grp
from django.db.models import (Model, EmailField, DateTimeField, DateField,
                            CharField, BooleanField, IntegerField, TextField,
                            DurationField,
                            ForeignKey, ManyToManyField, SET_NULL, CASCADE)

blank_null = {'blank':'True', 'null':'True'}
char60 = {'max_length':60}

class Utilisateur(User):
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)


class Group(grp):
    pass
