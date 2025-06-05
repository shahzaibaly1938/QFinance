from django.db import models

# Create your models here.
class Expense_category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Expense(models.Model):
    category = models.ForeignKey(Expense_category, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - Rs.{self.amount}"