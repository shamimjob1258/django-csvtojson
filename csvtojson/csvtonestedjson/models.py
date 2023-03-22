from django.db import models

class file_detail(models.Model):
    file_name = models.CharField(max_length=8, default='')
    file_type = models.TextField(blank=True, null=True)
    docfile = models.FileField(upload_to='csvtonestedjson/Input')

    def docfilename(self):
        return self.docfile.name
