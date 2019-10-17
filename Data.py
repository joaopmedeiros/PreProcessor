import pandas as pd
import numpy as np
import csv

# Ir testando tudo na prática agora com PJ
# Pensar numa forma melhor de criar o header e o trailer, talvez uma funcao que use as posicoes do layout, por enquanto é uma lista
# Documentar bem a criacao de dados, connection e query por exemplo precisam existir sempre juntas
# Coloquei uma opcao geral para todo arquivo na hora de preencher, verificar se nao deve ser personalizado para cada tipo de campo (ex: numericos com zero, texto com espaco)
# Verificar como ficam as importacoes de datas, por enquanto está tudo string

class Data:
    
    def __init__(self,
                 layout=None,
                 text_file=None,
                 csv=False,
                 csv_delimiter=';',
                 header='infer',
                 skipfooter=0,
                 decimal=',',
                 connection=None,
                 query=None):
        self.layout = layout
        self.text_file = text_file
        self.csv = csv
        self.csv_delimiter = csv_delimiter
        self.header = header
        self.skipfooter = skipfooter
        self.decimal = decimal
        self.connection = connection
        self.query = query
        self.df = None
        if connection:
            self._create_from_query()
        else:
            self._create_from_text_file()        
        
    def _create_from_text_file(self):
        if self.csv:
            self.df = pd.read_csv(self.text_file,
                                  sep=self.csv_delimiter,
                                  encoding='utf-8',
                                  header=self.header,
                                  dtype='object',
                                  decimal=',',
                                  names=[x for x in self.layout.get_field_names()
                                           if self.layout.get_field_atributtes(x).header
                                        ] if self.header==None else None
                                )
        else:
            self.df = pd.read_fwf(self.text_file,            
                 widths = [self.layout.get_field_atributtes(x).length 
                           for x in list(self.layout.get_field_names())
                           if not (self.layout.get_field_atributtes(x).header or self.layout.get_field_atributtes(x).trailler)
                           ],
                 names = [x for x in self.layout.get_field_names()
                          if not (self.layout.get_field_atributtes(x).header or self.layout.get_field_atributtes(x).trailler)
                         ],
                 dtype='object',
                 enconding = 'utf-8',
                 header=self.header,
                 skipfooter =self.skipfooter,
                 decimal = self.decimal
                )
            self.df = self.df.fillna('')

    def _create_from_query(self):
        cursor = self.connection.cursor()        
        cursor.execute(self.query)
        sql_columns =[x[0] for x in cursor.description]
        query_converted = [x for x in cursor.fetchall()]
        self.df = pd.DataFrame(query_converted,columns=sql_columns)

    def fill_fields(self,layout,consider_type=False,filler=' ',where='left'):
        # Implementar considerando diferentes filler para cada tipo
        for col in self.df.columns:
            length = layout.get_field_atributtes(self.df[col].name).length
            if where=='left':
                self.df[col] = self.df[col].apply(lambda x: length*filler if len(x)==0 else ((length - len(x))*filler) + x)
            elif where=='right':
                self.df[col] = self.df[col].apply(lambda x: length*filler if len(x)==0 else (x+(length - len(x))*filler))
            else:
                print("Select right or left to fill")

    def prepare_to_export_fwf(self,layout,header=None,trailler=None,consider_type=False,filler=' ',where='right'):
        # Header e trailer sao lista com os valores para serem inseridos
        
        self.fill_fields(layout,consider_type,filler,layout)

        self.df['all_'] = self.df[self.df.columns].apply(lambda x: ''.join(x), axis=1)
        if header:
            insert_header = ['' for x in self.df.columns[:-1]] + header
            self.df.loc[0] = insert_header
        if trailler:
            insert_trailler = ['' for x in self.df.columns[:-1]] + trailler
            self.df.loc[self.df.index.max()+1] = insert_trailler
        
    def export_to_txt_fwf(self,file_name):        
        np.savetxt(file_name, self.df['all_'], fmt='%s')
    
    def export_to_csv(self,file_name,csv_delimiter=";"):
        self.df.to_csv(file_name,index=False,sep=csv_delimiter)