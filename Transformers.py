# Criar as funcoes para ajustar aqui ou na importacao dos dados os formatos para conversao e arredondamentod e float e conversao de data

from datetime import datetime

def transform_date_itapeva(x):
    return x[4:8]+x[2:4]+x[0:2]+x[8:]

def transform_date_to_string(x,format):
    return x.strftime(format)

def transform_string_to_date(x,format):
    return datetime.strptime(x,format)