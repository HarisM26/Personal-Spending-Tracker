from django.db import models
from django.utils.translation import gettext_lazy as _
from expenditure.choices import *
from expenditure.models.limit import Limit
from expenditure.models.user import User
# from expenditure.helpers import get_default_categories_as_set


class SpendingCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    limit = models.OneToOneField(
        Limit, related_name='category', on_delete=models.CASCADE)
    # slug = models.SlugField()
    # parent = models.ForeignKey('self',blank=True, null=True ,related_name='children')
    # Reduce the remaining amount left of the spending limit

    # Checks if the category is not a default one
    @property
    def is_not_default(self):
        default_set = {'General', 'Groceries', 'Transport', 'Utilities'}
        self_set = {self.name}
        if not list(set(default_set) & set(self_set)):
            return True
        else:
            return False

    # Cannot delete a default category
    def delete(self, *args, **kwargs):
        if self.is_not_default:
            self.limit.delete()
            return super(SpendingCategory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class IncomeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
