from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def generate_pdf(ingredient_list):
    """Генерирует PDF-файл списка ингредиентов.
    Исподбзуется открытый шрифт DejaVuSerif.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shoplist.pdf"'
    font_path = f'{settings.BASE_DIR}/typeface/DejaVuSerif.ttf'
    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))

    p = canvas.Canvas(response)
    p.setFont('DejaVuSerif', 14)
    p.drawString(150, 800, 'Список ингредиентов:')
    p.line(150, 795, 400, 795)

    y = 750
    for ingredient in ingredient_list:
        p.drawString(
            50,
            y,
            f"{ingredient['total_amount']} "
            f"{ingredient['recipe__ingredients__measurement_unit']}.  "
            f"{ingredient['recipe__ingredients__name']};",
        )
        y -= 25
    p.showPage()
    p.save()
    return response
