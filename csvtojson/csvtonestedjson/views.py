from django.shortcuts import render
from django.views import View
from .forms import NameForm
from .file_process_pandas import FileConversion2
from django.http import FileResponse
import os, csv, io
from django.core.files.storage import FileSystemStorage

APPNAME = 'csvtonestedjson'

# The class get the csv file and convert it into json file format
class FileOperation(View) :

    def get(self, request) :
        form = NameForm()
        template_name = APPNAME + '/get_file.html'
        return render(request, template_name, {'form': form})

    def post(self, request) :
        template_name = APPNAME + '/get_file.html'
        form = NameForm(request.POST, request.FILES)
        fileobj = request.FILES.get('docfile', None)
        file_name = FileSystemStorage(location= os.getcwd()+"\\csvtonestedjson\\Input\\").save(fileobj.name, fileobj)
        ofile = FileConversion2(file_name)
        # Checking if file type is csv or not
        iscsvfile = ofile.file_type_validation()
        if iscsvfile.get('output_flg') != True :
            return render(request, template_name, context={'form': form, 'error_flg' : not(iscsvfile.get('output_flg')), 'error_msg' : iscsvfile.get('output_msg')})
        # Checking if file not empty
        isnonempthfile = ofile.file_non_empty()
        if isnonempthfile.get('output_flg') != True :
            return render(request, template_name, context={'form': form, 'error_flg' : not(isnonempthfile.get('output_flg')), 'error_msg' : isnonempthfile.get('output_msg')})
        # Checking if file structure correct or not
        isFileFormatCorrect = ofile.file_structure()
        if isFileFormatCorrect.get('output_flg') != True :
            return render(request, template_name, context={'form': form, 'error_flg' : not(isFileFormatCorrect.get('output_flg')), 'error_msg' : isFileFormatCorrect.get('output_msg')})
        # Converting given csv file into json file
        create_json_output = ofile.create_json()
        response = FileResponse(open(create_json_output.get('file'), 'rb'), as_attachment=True,filename=create_json_output.get('file'))

        return response
        # return render(request, template_name, context={'form': form, 'error_flg' : False, 'error_msg' : create_json_output})
