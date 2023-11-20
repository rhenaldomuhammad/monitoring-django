from django.db import models

# Create your models here.
class LogTable(models.Model):
    # Asumsikan tabel log_table memiliki kolom: timestamp, client_ip, dan message
    timestamp = models.DateTimeField()
    client_ip = models.CharField(max_length=100)
    message = models.CharField(max_length=300)

    class Meta:
        db_table = 'log_table'  # Menentukan nama tabel yang sesuai di database