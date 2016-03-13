#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import xml.parsers.expat
from ..models import PhysicalEntity
from .basicFunctions import BUF_SIZE

list_of_types_of_PhysicalEntity = ["Complex", "PhysicalEntity", "Complex",
"Dna", "DnaRegion", "Protein", 
"Rna", "RnaRegion", "SmallMolecule"]
#?? перенести ограничения на типы элементов в модель! А также использовать их в parserOwl методах!

class parserOwl:
    def __init__(self, el_file_owl, path_file):
        self.el_file_owl = el_file_owl # element of model fileOwl
        self.path_file = path_file # path to file
        self.flag_getting_element = False # this flag indicates: class collects data to save the element to BD
        self.current_field_name = ""
    
    # first handler functions for parser
    def start_element(self, name, attrs):
        #print('Start element:', name, attrs)
        #?? расширить на все типы, а не только Complex
        if name == "bp:Complex":
            try:
                self.element = PhysicalEntity.objects.get(file_owl=self.el_file_owl, id_name=attrs["rdf:ID"], kind_of="Complex")
                self.flag_getting_element = False # we do not change the collected data.
            except ObjectDoesNotExist:
                self.element = PhysicalEntity(file_owl=self.el_file_owl, id_name=attrs["rdf:ID"], kind_of="Complex")
                self.flag_getting_element = True
        
        if self.flag_getting_element and name == "bp:displayName":
            self.current_field_name = "display_name"
    
    # second handler functions for parser
    def end_element(self, name):
        if self.flag_getting_element and name == "bp:Complex":
            self.element.save()
            self.flag_getting_element = False
     
    # third handler functions for parser       
    def char_data(self, data):
        #print('Character data:', repr(data))
        if self.current_field_name != "":
            self.element.__dict__[self.current_field_name] = repr(data)
            self.current_field_name = ""
    
    def parse_owl(self):
        print("asd")
        parser = xml.parsers.expat.ParserCreate()
    
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data
    
        with open(self.path_file, 'rb') as f:
            xml_chunk = f.read(BUF_SIZE)
            while xml_chunk != b"":
                parser.Parse(xml_chunk)
                xml_chunk = f.read(BUF_SIZE)



""" TEST """
if (__name__ == '__main__'):
    file_name = "../data/RAF-Cascade.owl"

    def start_element(name, attrs):
        #print('Start element:', name, attrs)
        if name == "bp:Complex":
            print('Start element:', attrs["rdf:ID"], attrs)
    def end_element(name):
        if name == "bp:Complex":
            print('End element:', name)
    def char_data(data):
        #print('Character data:', repr(data))
        pass
        
    parser = xml.parsers.expat.ParserCreate()
    
    parser.StartElementHandler = start_element
    parser.EndElementHandler = end_element
    parser.CharacterDataHandler = char_data

    file_owl = open(file_name, 'rb')
    xml_chunk = file_owl.read(BUF_SIZE)
    while xml_chunk != b"":
        parser.Parse(xml_chunk)
        xml_chunk = file_owl.read(BUF_SIZE)
    file_owl.close()

