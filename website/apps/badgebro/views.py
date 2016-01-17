import StringIO
import qrcode
from django.core.files import File

# Create your views here.
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import DetailView

from website.apps.badgebro.models import Badge


class BadgePrintView(DetailView):
    queryset = Badge.objects.all()
    template_name = 'badgebro/badge_print.html'

    def get(self, request, *args, **kwargs):

        response = super(BadgePrintView, self).get(request, *args, **kwargs)

        return response

badge_print = BadgePrintView.as_view()
