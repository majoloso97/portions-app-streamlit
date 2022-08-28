import re

class PortionString():
  def __init__(
      self,
      units = ['taza', 'gramo', 'oz', 'unidad', 'cda', 'ml', 'cdita', 'clara'],
      num_regex = '\d*\.*\d+ *',
      symbols_to_replace = [('2 ½', '2.5'), 
                            ('1/4', '0.25'), 
                            ('1/2', '0.5'), 
                            ('¾', '0.75'), 
                            ('¼', '0.25'), 
                            ('½', '0.5'),
                            ('tz', 'taza'),
                            ('gamo', 'gramo'),
                            ('gr', 'gramo'),
                            ('onza', 'oz'),
                            ('rodaja', 'unidad'), 
                            ('pieza', 'unidad'), 
                            ('pequeñ', 'unidad'), 
                            ('entero', 'unidad'), 
                            ('maní', 'unidad'),
                            ('cc', 'ml')
                            ]
      ):
    self.units = units
    self.num_regex = num_regex
    self.symbols_to_replace = symbols_to_replace


  def clean(self, to_clean):
    no_symbols = self.replace_symbols(to_clean)
    decomposed_units = self.extract_units(no_symbols)
    return decomposed_units


  def validate_string(self, to_validate):
    for unit in self.units:
      if unit in to_validate:
        return True
    return False
  

  def replace_symbols(self, to_clean):
    for symbol in self.symbols_to_replace:
      to_clean = to_clean.replace(symbol[0], symbol[1])

    return to_clean


  def decompose_units(self, to_extract):
    key = re.split(self.num_regex, to_extract)
    key = [s for s in key if len(s)>0][0]
    
    value = re.split(' *' + key, to_extract)
    value = [s for s in value if len(s)>0][0]
    
    return (key, value)


  def extract_units(self, to_clean):
    data = []
    for unit in self.units:
      pattern = self.num_regex + unit
      dirty = re.findall(pattern, to_clean)
      
      if len(dirty) > 0: 
        cleaned = self.decompose_units(dirty[0]) 
        data.append(cleaned)

    portions = {key: value for key, value in data}

    return portions
