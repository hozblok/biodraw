from django.shortcuts import render
import json

#from django.http import HttpResponse
#from django.template import RequestContext, loader

def test1(request):
    with open("draw/data/miserables.json") as data_file:
        #test_draw = [{"id": 1, "text": 'Hi!',}, {"id": 2, "text": 'This is the test!',}]
        json_string_data = json.dumps(json.loads(data_file.read()))
    #template = loader.get_template('draw/index.html')
    #context = RequestContext(request, {
    #    'test_draw': test_draw,
    #})
    #return HttpResponse(template.render(context))
    context = {
    'json_string_data': json_string_data,
    }
    return render(request, 'draw/index.html', context)
    
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
