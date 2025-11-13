from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd
import csv
import time
from typing import List, Tuple

# Cria um geolocalizador reutilizável para evitar re-criação em cada chamada
geolocator = Nominatim(user_agent="my_geocoding_app")


def get_coordinates_from_address(address: str, timeout: int = 5, max_retries: int = 3) -> Tuple[float, float]:
    """Tenta obter coordenadas para um endereço com alguns retries em caso de timeout.

    Retorna (latitude, longitude) ou (None, None) se não encontrar.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            location = geolocator.geocode(address, timeout=timeout)
            if location:
                return location.latitude, location.longitude
            else:
                # Não encontrou o endereço
                return None, None
        except GeocoderTimedOut:
            attempt += 1
            wait = 1 * attempt
            time.sleep(wait)
        except GeocoderServiceError:
            # Erro do serviço — não adianta continuar
            return None, None

    return None, None


def process_ods_file(file_path: str, city_suffix: str = 'Pelotas - RS') -> List[str]:
    """Lê todas as abas de um arquivo .ods e coleta os valores da coluna 'Endereço'.

    Adiciona o sufixo de cidade quando o endereço for texto e não contiver o nome da cidade.
    """
    column_data: List[str] = []
    xls = pd.ExcelFile(file_path, engine='odf')
    sheet_names = xls.sheet_names

    for sheet_name in sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        if 'Endereço' in df.columns:
            for address in df['Endereço']:
                if isinstance(address, str):
                    if city_suffix.split()[0] not in address:
                        address = f"{address}, {city_suffix}"
                    column_data.append(address)
                else:
                    print(f"Endereço inválido na aba '{sheet_name}': {address}")
        else:
            print(f"Coluna 'Endereço' não encontrada na aba '{sheet_name}'.")

    return column_data


def process_file(file_path: str, output_filename: str = 'enderecos_com_coordenadas.csv') -> Tuple[str, int]:
    """Processa o arquivo ODS e gera um CSV com coordenadas.

    Retorna (output_filename, erros_count).
    """
    column_data = process_ods_file(file_path)
    erros = 0

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['WKT', 'Endereço']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for address in column_data:
            lat, lon = get_coordinates_from_address(address)
            if lat is not None and lon is not None:
                writer.writerow({'WKT': f'({lon} {lat})', 'Endereço': address})
                print(f"Coordenadas para '{address}': Latitude={lat}, Longitude={lon}")
            else:
                writer.writerow({'WKT': f'(None None)', 'Endereço': address})
                print(f"Não foi possível obter coordenadas para '{address}'.")
                erros += 1

    print(f"Arquivo CSV com coordenadas gerado: {output_filename}")
    print(f"Erros Totais: {erros}")
    return output_filename, erros


if __name__ == '__main__':
    # Execução padrão via CLI
    file_path = 'sample/Cópia de Atividade 1 PET.ods'
    process_file(file_path)