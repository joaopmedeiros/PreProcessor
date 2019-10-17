import csv
from collections import defaultdict
import json
import sys


# Testar a conversao do multcob



def transform_csv_to_json(csv_file):
    with open (csv_file, 'r', encoding='utf-8') as f:
        csv_list = [x for x in csv.reader(f,delimiter=';')]
    
    attributes = csv_list[0]
    layout_json = defaultdict(dict)
    
    for i in csv_list[1:]:
        dict_atr = defaultdict(str)
        for j in range(1,len(attributes)):
            if attributes[j] == 'start_pos' or attributes[j] == 'length' or attributes[j] == 'end_pos':
                dict_atr[attributes[j]] = int(i[j])
            else:
                dict_atr[attributes[j]] = i[j] 
        layout_json[i[0]] = dict_atr
    
    with open (csv_file[:-3]+'json', 'w', encoding='utf-8') as f:
        json.dump(layout_json,f, ensure_ascii=False, indent=True)


def mcob_make_json(linha):
    with open('layout_json.json') as json_arq:
        LayoutJson = json.load(json_arq)
        LayoutJson[linha['nome']] = LayoutJson.pop('Nome') #ajusta o nome
        LayoutJson[linha['nome']]['required'] = "True"
        LayoutJson[linha['nome']]['data_type'] = '' #linha['tipo'] precisa fazer um depara
        LayoutJson[linha['nome']]['default'] = ""
        LayoutJson[linha['nome']]['start_pos'] = linha['posicao']
        LayoutJson[linha['nome']]['length'] = linha['tamanho']
        LayoutJson[linha['nome']]['end_pos'] = linha['posicao']+linha['tamanho']
        LayoutJson[linha['nome']]['formating'] = ""
        LayoutJson[linha['nome']]['header'] = "False"
        LayoutJson[linha['nome']]['trailler'] = "False"
        LayoutJson[linha['nome']]['obs'] = ""
        LayoutJson[linha['nome']]['decimal_point'] = "False"
    return LayoutJson

def transform_multcob_to_json(file_name):
    with open(mcob_file, encoding='utf8') as json_file:
        MultcobJson = json.load(json_file)
    lista = {}
    for linha in MultcobJson['colunas']:
        if not 'CC' in linha['nome'].upper():
            lista.update(mcob_make_json(linha))
    json_string = json.dumps(lista)
    with open('layout_'+mcob_file,'w') as saida:
        arq = saida.writelines(json_string)

file_name = sys.argv[1]
option = sys.argv[2]

if option == 'csv':
    transform_csv_to_json(file_name)
elif option == 'multcob':
    transform_multcob_to_json(file_name)
else:
    print("Selecione uma opcao de conversao, 'csv' ou 'multcob'")