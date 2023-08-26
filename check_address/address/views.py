from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from address.forms import *
from address.models import *
from django.http.response import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import os
import csv
import openpyxl
from typing import Tuple
# Create your views here.

model_path = os.path.join('check_streets', 'ML', 'model.pt')

class OutputData:
    def __init__(self, object_id, text, prob) -> None:
        self.object_id = object_id
        self.text = text
        self.probability = prob


def updata_address(address: str):
    # Здесь должна быть модель
    list_ans = []
    
    return list_ans


def read_csv(file: str) -> list:
    with open(file, encoding='cp1251', errors='ignore', mode='r') as f:
        # encoding='cp1251'
        reader = csv.reader(f)
        file_content = [''.join(row) for row in reader]
    return file_content


def read_excel(file: str) -> list:
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active
    file_content = [row for row in sheet.iter_rows(values_only=True)]
    return file_content


def slider(request):
    return render(request, '-vslider.html')


def megamen(request):
    return render(request, '-vmegamen.html')


class CheckTextView(View):
    context = {}

    def get(self, request):
        form_text = AddressTextForm()
        self.context['form_text'] = form_text
        return render(request, 'text_input.html', context=self.context)

    @method_decorator(login_required)
    def post(self, request):
        form_text = AddressTextForm(request.POST)
        if form_text.is_valid():
            object = form_text.save(commit=False)
            object.user = request.user
            list_ans = updata_address(object.text)
            object.corrected_text = list_ans[0].text
            object.save()
            self.context['addresses'] = list_ans
            return render(request, 'text_input.html', self.context)
        else:
            return render(request, 'text_input.html', context=self.context)


class CheckFileView(View):
    context = {}

    def get(self, request):
        form_file = AddressFileForm()
        self.context['form_file'] = form_file
        self.context['object'] = None
        return render(request, 'file_input.html', context=self.context)

    @method_decorator(login_required)
    def post(self, request):
        form_file = AddressFileForm(request.POST, request.FILES)
        if form_file.is_valid():
            input_request = form_file.save(commit=False)
            input_request.user = request.user
            input_request.save()
            output_request = AddressFile.objects.filter(
                user=request.user).latest('id')
            format_file = output_request.file.path[-3:]
            match format_file:
                case 'csv':
                    list_address = read_csv(output_request.file.path)
                case 'xls' | 'lsx':
                    list_address = read_excel(output_request.file.path)
                    print('xls')
                case _:
                    raise Http404
            for i in range(len(list_address)):
                list_address[i] = updata_address(list_address[i])
            response = HttpResponse(
                list_address, content_type=f'application/{format_file}')
            response['Content-Disposition'] = f'attachment; filename="answer.{format_file}"'
            return response
        else:
            raise Http404
