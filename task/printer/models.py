from django.db import models

class Printer(models.Model): 
    KITCHEN_TYPE = 'kitchen'
    CLIENT_TYPE = 'client'

    CHECK_TYPES = [
        (KITCHEN_TYPE, 'Kitchen'),
        (CLIENT_TYPE, 'Client')
    ]
    name = models.CharField(max_length=150)
    api_key = models.CharField(max_length=100, unique=True)
    check_type = models.CharField(max_length=100, choices=CHECK_TYPES)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name

class Check(models.Model):
    NEW_STATUS = 'new'
    RENDERED_STATUS = 'rendered'
    PRINTED_STATUS = 'printed'

    CHECK_STATUSES = [
        (NEW_STATUS, 'New'),
        (RENDERED_STATUS, 'Rendered'),
        (PRINTED_STATUS, 'Printed'),
    ]
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=Printer.CHECK_TYPES)
    order = models.JSONField()
    status = models.CharField(max_length=150, choices=CHECK_STATUSES, default=NEW_STATUS)
    pdf_file = models.FileField(upload_to='media/pdf', null=True, blank=True)
    

