import xml.parsers.expat

from django.core.exceptions import ObjectDoesNotExist
from ..models import PhysicalEntity
from .utils import BUFF_SIZE

PREFIX_CLASSES = "bp"

class parserOwl:
    def __init__(self, el_file_owl):
        self.el_file_owl = el_file_owl # element of model fileOwl
        self.path_file = el_file_owl.path_name # path to file
        self.flag_getting_element = False # this flag indicates: class collects data to save the element to BD
        self.current_field_name = ""
        self.list_of_types_of_PhysicalEntity = list(map(lambda x: ":".join((PREFIX_CLASSES, x[0])),
                                                    PhysicalEntity.TYPES_OF_PHYSICALENTITY))
    
    # first handler functions for parser - This is the opening tag
    def start_element(self, name, attrs):
        
        #+- check for the tag belongs to basic substances
        if name in self.list_of_types_of_PhysicalEntity:
            kind_of = name.split(":", 1)[1]
            id_in_file = attrs["rdf:ID"].replace(kind_of, "")
            self.element, created = PhysicalEntity.objects.get_or_create(file_owl=self.el_file_owl, id_name=attrs["rdf:ID"],
                  defaults={"kind_of": kind_of, "display_name" : "", "id_in_file": id_in_file}) #'id_in_file': id_in_file
            if self.element.display_name != "":
                self.flag_getting_element = False # we do not change the collected data.
            else:
                self.flag_getting_element = True # element is not completely filled
                self.element.kind_of = kind_of
        
        #+ check for secondary tags and get them
        self.current_field_name = "" # == the tag name, which is the first in the queue for processing
        if self.flag_getting_element and name == "bp:displayName":
            self.current_field_name = "display_name"
        elif self.flag_getting_element and name == "bp:comment":
            self.current_field_name = "comment"
        elif self.flag_getting_element and name == "bp:component": # ex. component of Complex
            id_name = attrs["rdf:resource"][1:]
            new_element, created = PhysicalEntity.objects.get_or_create(file_owl=self.el_file_owl, id_name=id_name)
            self.element.component.add(new_element)
        elif self.flag_getting_element and name == "bp:memberPhysicalEntity": # ex. Protein-doughter of other Protein
            id_name = attrs["rdf:resource"][1:]
            new_element, created = PhysicalEntity.objects.get_or_create(file_owl=self.el_file_owl, id_name=id_name)
            self.element.member_physical_entity.add(new_element)
        else: # unknown field
            pass # === self.current_field_name = ""
        #- check for secondary tags and get them
     
    # third handler functions for parser - Data between the opening and closing tag
    def char_data(self, data):
        if self.current_field_name != "": # ex. == "display_name", "comment"
            self.element.__dict__[self.current_field_name] = str(data)
            self.current_field_name = ""
    
    # second handler functions for parser - This is the closing tag
    def end_element(self, name):
        if self.flag_getting_element and name in self.list_of_types_of_PhysicalEntity:
            self.element.save()
            self.flag_getting_element = False
    
    # main function
    def parse_owl(self):
        parser = xml.parsers.expat.ParserCreate()
    
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.char_data
    
        with open(self.path_file, 'rb') as f:
            xml_chunk = f.read(BUFF_SIZE) # lets read stuff in 64kb chunks!
            while xml_chunk != b"":
                parser.Parse(xml_chunk)
                xml_chunk = f.read(BUFF_SIZE) # lets read stuff in 64kb chunks!



"""
TEST 
TEST
TEST
"""
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
    xml_chunk = file_owl.read(BUFF_SIZE)
    while xml_chunk != b"":
        parser.Parse(xml_chunk)
        xml_chunk = file_owl.read(BUFF_SIZE)
    file_owl.close()

