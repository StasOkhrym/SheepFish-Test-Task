from rest_framework import renderers


class PDFRenderer(renderers.BaseRenderer):
    media_type = "application/pdf"
    format = "pdf"
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
