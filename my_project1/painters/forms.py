from django.forms import ModelForm
from .models import Painter

class PainterForm(ModelForm):
    class Meta:
        model = Painter
        fields = '__all__'