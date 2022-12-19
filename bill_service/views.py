from rest_framework import viewsets, status
from rest_framework.response import Response

from SheepFish_test_task.celery import app
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
        order = data.get("order", {})
        checks = Check.objects.filter(point=point)

        for check in checks:
            if check["order_id"] == order["order_id"]:
                return Response(
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
                    check_for_print = Check.objects.create(**attrs)
                    app.send_task("bill_service.tasks.render_pdf_kitchen", check_for_print)
                else:
                    attrs = {
                        "printer": printer,
                        "type": "client",
                        "status": data.get("status", "new"),
                        "order": order,
                    }
                    check_for_print = Check.objects.create(**attrs)
                    app.send_task("bill_service.tasks.render_pdf_client", check_for_print)

            return Response(
                {"check": "Чек успішно створено"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"check": "Принтер не знайдено"},
                status=status.HTTP_404_NOT_FOUND,
            )

    