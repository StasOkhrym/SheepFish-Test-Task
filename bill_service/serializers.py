from rest_framework import serializers

from bill_service.models import Point, Printer, Check


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ("id", "name")


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = (
            "id",
            "check_type",
            "point",
        )


class CheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = (
            "id",
            "point",
            "type",
            "order",
            "status",
            "pdf_file",
        )
