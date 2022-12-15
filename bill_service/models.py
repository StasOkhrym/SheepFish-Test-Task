from django.db import models

TYPE_CHOICES = [
    ("kitchen", "kitchen"),
    ("client", "client"),
]

STATUS_CHOICES = [
    ("new", "new"),
    ("rendered", "rendered"),
    ("printed", "printed"),
]


class Point(models.Model):
    name = models.CharField(max_length=64)


class Printer(models.Model):
    name = models.CharField(max_length=64)
    check_type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        related_name="printers"
    )


class Check(models.Model):
    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        related_name="checks"
    )
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    order = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES)
    pdf_file = models.FileField(null=True, blank=True, upload_to="media/pdf")
