from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from SheepFish_test_task.celery import app


def get_pdf_check(template_source, context):
    template = get_template(template_source)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def save_to_pdf_field(check, response, pdf_name):
    if response.status_code == 200:
        check.status = "rendered"
        check.save()
    pdf_field = check.pdf_file
    buffer = BytesIO()
    buffer.write(response.content)
    pdf_file = ContentFile(buffer.getvalue())
    pdf_field.save(pdf_name, InMemoryUploadedFile(pdf_file, None, pdf_name, "application/pdf", pdf_file.tell, None))
    check.save()


def get_order_number_and_dict(check):
    order_dict = {}
    order_dict.update(check.order)
    order_number = order_dict.pop("order_number")
    return order_number, order_dict


def get_order_number_dict_and_price(check):
    order_number, order = get_order_number_and_dict(check.order)
    total_price = 0
    for item in order.values():
        total_price += int(item["price"])
    return order_number, total_price, order


@app.task
def render_pdf_kitchen(check):
    order_number, order = get_order_number_and_dict(check)
    pdf_name = f"{order_number}_{check.type}.pdf"
    context = {
        "order_number": order_number,
        "order": order
    }
    response = get_pdf_check(settings.KITCHEN_CHECK_TEMPLATE, context=context)
    save_to_pdf_field(check, response, pdf_name)


@app.task
def render_pdf_client(check):
    order_number, total_price, order = get_order_number_dict_and_price(check)
    pdf_name = f"{order_number}_{check.type}.pdf"
    context = {
        "order_number": order_number,
        "total_price": total_price,
        "order": order
    }
    response = get_pdf_check(settings.CLIENT_CHECK_TEMPLATE, context=context)
    save_to_pdf_field(check, response, pdf_name)
