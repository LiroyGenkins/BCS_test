from django.db import models

class Transaction(models.Model):
    transaction_hash = models.CharField('хеш транзакции', max_length = 100)
    transaction_sum = models.FloatField('сумма транзакции', max_length = 20)
    transaction_description = models.TextField('описание транзакции', max_length = 200, default="")

    def __str__(self):
        return self.transaction_hash

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"