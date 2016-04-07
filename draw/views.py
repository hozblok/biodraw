#from django.http import HttpResponse
#from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json
import datetime

from .models import FileOwl
from .models import PhysicalEntity

from .src.parserOwl import parserOwl

from .src.utils import md5
from .src.utils import sha1
from .src.utils import BUFF_SIZE
from .src.utils import random_id

from .forms import UploadFileForm

#_______________________________________________________________________________#
#Перенести логику целиком в .src.parserOwl. Вызов происходит теперь в uploadFile|
#_______________________________________________________________________________#
def test1(request):
    suffix_file_name = "RAF-Cascade.owl"
    file_name = "draw/data/" + suffix_file_name
    
    file_sha1 = sha1(file_name)
    try:
        el_file_owl = FileOwl.objects.get(sha1=file_sha1)
    except ObjectDoesNotExist:
        prefix_for_file_name = random_id()
        file_name_physical = "draw/data/" + prefix_for_file_name + suffix_file_name
        el_file_owl = FileOwl(original_name=suffix_file_name, path_name=file_name_physical, sha1=file_sha1, pub_date=datetime.datetime.now())
        el_file_owl.save()
    # http://djbook.ru/rel1.7/topics/http/file-uploads.html
    #?? не окончено, нужно сделать кнопку и допилить механизм, который будет забирать файлы от клиента
    
    
    # parse owl-xml data and collect to database
    parser = parserOwl(el_file_owl, file_name)
    parser.parse_owl()
    
    
    
    
    
    def name_for_js(kind_of, name): 
        return (".".join(["flare", kind_of, "cluster", name]))
    def dict_one_element_for_js(el):
        return ({"name": name_for_js(el.kind_of, el.id_name),
        "id_name": el.display_name,
        "size": 200,
        "imports":[name_for_js(comp.kind_of, comp.id_name) for comp in el.component.all()]
        })
    query_set = PhysicalEntity.objects.filter(file_owl_id=el_file_owl).order_by('id_name')
    data_for_js = list(map(dict_one_element_for_js, query_set))
    
    #with open("draw/data/flare-imports.json") as data_file:
        #test_draw = [{"id": 1, "text": 'Hi!',}, {"id": 2, "text": 'This is the test!',}]
        #json_string_data = json.dumps(json.loads(data_file.read()))
    #template = loader.get_template('draw/index.html')
    #context = RequestContext(request, {
    #    'test_draw': test_draw,
    #})
    #return HttpResponse(template.render(context))
    
    json_string_data = json.dumps(data_for_js)
    context = {
    'json_string_data': json_string_data,
    }
    return render(request, 'draw/index_test3_itog.html', context)
    
def test2(request):
    python_object = {
    "name": "Top Level",
    "parent": "null",
    "children": [
      {
        "name": "Level yosh: A",
        "parent": "Top Level",
        "children": [
          {
            "name": "Son of A",
            "parent": "Level 2: A"
          },
          {
            "name": "Daughter of A",
            "parent": "Level 2: A"
          }
        ]
      },
      {
        "name": "Level 2: B",
        "parent": "Top Level"
      }
    ]
    }
    json_string = json.dumps(python_object)  
    context = {
    'json_string': json_string
    }
    return render(request, 'draw/index_test2.html', context)

@login_required	
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			#Получаем логин пользователя
			username = request.user.username
			#Получаем файл. Возвращает объект UploadedFile. См. описание тут: https://docs.djangoproject.com/en/1.9/ref/files/uploads/
			#У него есть нужный метод multiple_chunks\chunks для считывание целым куском, либо по кускам.
			file = request.FILES['file']
			#тут создаём парсер и веселимся. Я потом раскидаю в более логичном порядке.
			return HttpResponseRedirect('/draw/')
	else:
		form = UploadFileForm()
	return render(request, 'draw/index_upload.html', {'form': form})