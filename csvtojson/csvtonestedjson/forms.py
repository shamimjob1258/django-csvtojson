from django.forms import ModelForm, Textarea, FileField
from . import models

class NameForm(ModelForm):
    docfile = FileField(
        label='Select File',
        required=True
    )
    class Meta:
        model = models.file_detail
        fields = ['docfile']
        exclude = ('file_name','file_type')
