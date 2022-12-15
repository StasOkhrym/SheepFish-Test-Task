from django.http import JsonResponse
from rest_framework import viewsets, status
from bill_service.serializers import (
    PointSerializer,
    PrinterSerializer,
    CheckSerializer,
)
from bill_service.models import Point, Printer, Check


class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        point = data.get("point", None)
        order = {}  # TODO : make it json
        checks = Check.objects.filter(point=point)

        for check in checks:
            if check["order_id"] == order["order_id"]:
                return JsonResponse(
                    {"order": "Таке замовлення вже існує"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if (printers := Printer.objects.filter(point=point)).exists():
            for printer in printers:
                if printer.check_type == "kitchen":
                    attrs = {
                        "printer": printer,
                        "type": "kitchen",
                        "status": data.get("status", "new"),
                        "order": order,
                    }
                    Check.objects.create(**attrs)
                else:
                    attrs = {
                        "printer": printer,
                        "type": "client",
                        "status": data.get("status", "new"),
                        "order": order,
                    }
                    Check.objects.create(**attrs)

            return JsonResponse(
                {"check": "Чек успішно створено"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return JsonResponse(
                {"check": "Принтер не знайдено"},
                status=status.HTTP_404_NOT_FOUND,
            )
