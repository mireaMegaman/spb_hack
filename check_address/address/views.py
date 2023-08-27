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
from sentence_transformers import SentenceTransformer
from ML.infer import encode_one_record, predict
from ML.prepare_text import clean_text
import torch
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
# Create your views here.

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#model_path = os.path.join('check_streets', 'ML', 'model.pt')

def seed_everything(seed):
    import random
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

seed_everything(seed=42)


def updata_address(address: str):
    user_address = str(address) # user input
    clean_data = clean_text(user_address)
    embedding = encode_one_record(clean_data, model)
    label, place, chance = predict(embedding)
    return f'{label} {" ".join(place)}\n', chance


def read_csv(file: str) -> list:
    with open(file, errors='ignore', mode='r') as f:
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
        self.context['address'] = ''
        self.context['chance'] = ''
        return render(request, 'text_input.html', context=self.context)

    @method_decorator(login_required)
    def post(self, request):
        form_text = AddressTextForm(request.POST)
        if form_text.is_valid():
            object = form_text.save(commit=False)
            object.user = request.user
            ans, chance = updata_address(object.text)
            object.corrected_text = ans
            object.save()
            self.context['address'] = ans
            self.context['chance'] = chance
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
                case _:
                    raise Http404
            for i in range(len(list_address)):
                list_address[i], chance = updata_address(list_address[i])
            response = HttpResponse(
                list_address, content_type=f'application/{format_file}')
            response['Content-Disposition'] = f'attachment; filename="answer.{format_file}"'
            return response
        else:
            raise Http404
