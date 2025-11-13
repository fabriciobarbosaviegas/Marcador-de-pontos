from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd
import csv

erros = 0

# Função para obter coordenadas de um endereço
def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="my_geocoding_app") 
    try:
        location = geolocator.geocode(address, timeout=5) 
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not find coordinates for: {address}")
            return None, None
    except GeocoderTimedOut:
        print(f"Geocoding service timed out for: {address}")
        return None, None
    except GeocoderServiceError as e:
        print(f"Geocoding service error for {address}: {e}")
        return None, None

# Função para processar todas as abas e colunas de endereços de um arquivo ODS
def process_ods_file(file_path):
    column_data = []
    
    # Lê o arquivo .ods usando pandas
    xls = pd.ExcelFile(file_path, engine='odf')  # Use engine='odf' para .ods
    sheet_names = xls.sheet_names  # Obtém os nomes das abas na planilha
    
    for sheet_name in sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Verifica se a coluna 'Endereço' existe
        if 'Endereço' in df.columns:
            # Adiciona os valores da coluna 'Endereço' e ajusta o formato
            for address in df['Endereço']:
                # Adiciona a cidade "Pelotas - RS" se não estiver presente no endereço
                if isinstance(address, str):
                    if 'Pelotas' not in address:
                        address += ', Pelotas - RS'
                    column_data.append(address)
                else:
                    print(f"Endereço inválido na aba '{sheet_name}': {address}")
        else:
            print(f"Coluna 'Endereço' não encontrada na aba '{sheet_name}'.")
    
    return column_data

# Processa o arquivo ODS e obtém os endereços
file_path = 'sample/Cópia de Atividade 1 PET.ods'
column_data = process_ods_file(file_path)

# Criar e escrever um novo CSV com as coordenadas
output_filename = 'enderecos_com_coordenadas.csv'

with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['WKT', 'Endereço']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Escreve o cabeçalho
    
    for address in column_data:
        lat, lon = get_coordinates_from_address(address)
        if lat and lon:
            # Escreve a linha no CSV com as coordenadas
            writer.writerow({'WKT':f'({lon} {lat})', 'Endereço': address})
            print(f"Coordenadas para '{address}': Latitude={lat}, Longitude={lon}")
        else:
            # Caso não consiga obter as coordenadas, escreve o endereço e "None"
            writer.writerow({'WKT':f'(None None)', 'Endereço': address})
            print(f"Não foi possível obter coordenadas para '{address}'.")
            erros += 1

print(f"Arquivo CSV com coordenadas gerado: {output_filename}")
print(f"Erros Totais: {erros}")