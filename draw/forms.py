from django import forms
from functools import reduce

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file',
        help_text='max. 10 megabytes')
        
        
    def clean_file(self):
        #поверхностная проверка на совпадение форматов.
        file_name = self.cleaned_data['file'].name
        correct_formats = ('owl', 'xml')
        
        def isFound(result, nextFormat):
            return result or file_name[-len(nextFormat):] == nextFormat 
            
        if reduce(isFound, correct_formats, False):
            return self.cleaned_data['file']
        else:
            raise forms.ValidationError('incorrent file format', 'invalid')
            
