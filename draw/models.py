from django.db import models

"""
Information about the uploaded file in the next format:
http://www.biopax.org/release/biopax-level3.owl
"""
class FileOwl(models.Model):
    original_name = models.CharField(max_length=200)
    path_name = models.CharField(max_length=210)
    sha1 = models.CharField(unique=True, max_length=40)
    pub_date = models.DateTimeField()
    def __str__(self):
        return self.path_name

"""
Definition: A pool of molecules or molecular complexes. 

Comments: Each PhysicalEntity is defined by a  sequence or structure based on an EntityReference AND any set of Features that are given. For example,  ser46 phosphorylated p53 is a physical entity in BioPAX defined by the p53 sequence and the phosphorylation feature on the serine at position 46 in the sequence.  Features are any combination of cellular location, covalent and non-covalent bonds with other molecules and covalent modifications.  

For a specific molecule to be a member of the pool it has to satisfy all of the specified features. Unspecified features are treated as unknowns or unneccesary. Features that are known to not be on the molecules should be explicitly stated with the "not feature" property. 
A physical entity in BioPAX  never represents a specific molecular instance. 

Physical Entity can be heterogenous and potentially overlap, i.e. a single molecule can be counted as a member of multiple pools. This makes BioPAX semantics different than regular chemical notation but is necessary for dealing with combinatorial complexity. 

Synonyms: part, interactor, object, species

Examples: extracellular calcium, ser 64 phosphorylated p53
"""
class PhysicalEntity(models.Model):
    file_owl = models.ForeignKey(FileOwl)
    id_name = models.CharField(max_length=200) # PhysicalEntity1, Complex10, Protein7 etc.
    kind_of = models.CharField(max_length=20) # PhysicalEntity, Complex, Dna, DnaRegion, Protein, Rna, RnaRegion, SmallMolecule
    display_name = models.TextField(blank=True)
    component = models.ManyToManyField('self', null=True, blank=True, symmetrical=False, related_name='self_components')
    member_physical_entity = models.ManyToManyField('self', null=True, blank=True, symmetrical=False)
    comment = models.TextField(null=True, blank=True)
    def __str__(self):
        return("{}: {}".format(self.id_name, self.display_name))
