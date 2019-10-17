import json
from collections import namedtuple

class Layout:
    
    def __init__(self,json_file):
        self.json_file = json_file
        self.layout = None
        
        self._create_from_json()
        if not self._validate_layout_fields():
            raise ValueError("Field properties are not valid, check layout")

    def _create_from_json(self):
        with open(self.json_file, encoding='utf-8') as file:          
            self.layout = json.load(file)
    
    def _validate_layout_fields(self): 
        for i in self.layout.values():            
            try:
                if i["start_pos"] < 1 or i["end_pos"] < 1:
                    return False
                if not isinstance(i["start_pos"], int):
                    return False
                if not isinstance(i["length"], int):
                    return False
                if not isinstance(i["end_pos"], int):
                    return False
                return True
            except: 
                raise ValueError("Field propertys are not valid, check layout")                
        
    def get_field_names(self):
        return self.layout.keys()    
    
    def get_field_atributtes(self, field_name):    
        name = field_name
        try:
            required = True if self.layout[field_name]["required"]=="True" or self.layout[field_name]["required"] is True else False
            data_type = self.layout[field_name]["data_type"]
            default = self.layout[field_name]["default"]
            start_pos = self.layout[field_name]["start_pos"]
            length = self.layout[field_name]["length"]
            end_pos = self.layout[field_name]["end_pos"]
            formating = self.layout[field_name]["formating"]
            header = True if self.layout[field_name]["header"]=="True" or self.layout[field_name]["header"] is True else False
            trailler = True if self.layout[field_name]["trailler"]=="True" or self.layout[field_name]["trailler"] is True else False
            obs = self.layout[field_name]["obs"]
            decimal_point = True if self.layout[field_name]["decimal_point"]=="True" or self.layout[field_name]["decimal_point"] is True else False
            FieldAtributtes = namedtuple('FieldAtributtes', 'name required data_type default start_pos length end_pos formating header trailler obs decimal_point')
        except:
            raise KeyError("Field or field porperty not found in layout")
        return FieldAtributtes(name=field_name,
                           required=required,
                           data_type=data_type,
                           default=default, 
                           start_pos=start_pos,
                           length=length,
                           end_pos=end_pos,
                           formating=formating,
                           header=header, 
                           trailler=trailler,
                           obs=obs,
                           decimal_point=decimal_point)