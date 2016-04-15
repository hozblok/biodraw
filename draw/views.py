from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import json

from .models import FileOwl
from .models import PhysicalEntity

from .src.parserOwl import parserOwl

from .forms import UploadFileForm

from .src.uploadedFileHandler import handle_uploaded_file

#_______________________________________________________________________________#
#Перенести логику целиком в .src.parserOwl. Вызов происходит теперь в uploadFile|
#_______________________________________________________________________________#
def test1(request):

    #+затычка
    el_file_owl = FileOwl.objects.get(sha1="648df295bd548740d80e0b5aa9166d4859cc6fad")
    #-
    
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
            
            user = request.user
            # get file. (class UploadedFile). description: https://docs.djangoproject.com/en/1.9/ref/files/uploads/
            uploaded_file = request.FILES['file']
            # save file to media/.../ and save information about file to db
            db_file_owl = handle_uploaded_file(uploaded_file, user)
            print("### db_file_owl: ###", db_file_owl)
            
            # parse owl-xml data and collect to database
            parser = parserOwl(db_file_owl)
            parser.parse_owl()
            
            return HttpResponseRedirect('/draw')
    else:
        form = UploadFileForm()
    return render(request, 'draw/index_upload.html', {'form': form})
