from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pandas as pd
import csv
import time
from typing import List, Tuple, Callable

geolocator = Nominatim(user_agent="pointMap")


def get_coordinates_from_address(address: str, timeout: int = 5, max_retries: int = 3) -> Tuple[float, float]:
    attempt = 0
    while attempt < max_retries:
        try:
            location = geolocator.geocode(address, timeout=timeout)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except GeocoderTimedOut:
            attempt += 1
            wait = 1 * attempt
            time.sleep(wait)
        except GeocoderServiceError:
            return None, None

    return None, None


def process_ods_file(file_path: str, city_suffix: str = 'Pelotas - RS') -> List[str]:
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


def process_file(file_path: str, output_filename: str = 'enderecos_com_coordenadas.csv', logger: Callable[[str], None] = None) -> Tuple[str, int, List[str]]:
    column_data = process_ods_file(file_path)
    erros = 0
    failed_addresses: List[str] = []

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['WKT', 'Endereço']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for address in column_data:
            lat, lon = get_coordinates_from_address(address)
            if lat is not None and lon is not None:
                writer.writerow({'WKT': f'({lon} {lat})', 'Endereço': address})
                msg = f"Coordenadas para '{address}': Latitude={lat}, Longitude={lon}"
                if logger:
                    logger(msg)
                else:
                    print(msg)
            else:
                msg = f"Não foi possível obter coordenadas para '{address}'."
                if logger:
                    logger(msg)
                else:
                    print(msg)
                erros += 1
                failed_addresses.append(address)

    summary_msg = f"Arquivo CSV com coordenadas gerado: {output_filename}"
    if logger:
        logger(summary_msg)
        logger(f"Erros Totais: {erros}")
    else:
        print(summary_msg)
        print(f"Erros Totais: {erros}")

    return output_filename, erros, failed_addresses