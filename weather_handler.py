import requests
from influxdb import InfluxDBClient
import sys
import os
import logging
from dotenv import load_dotenv

#Init logging and variables
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
load_dotenv()

headers = {'User-Agent': 'weather_handler'}
params = (
    ('altitude', '0'),
    ('lat', '60.51316822249571'),
    ('lon', '22.26266254250938')
)
URL = 'https://api.met.no/weatherapi/nowcast/2.0/complete'
HOST = os.getenv('INFLUX_HOST')
PORT = os.getenv('INFLUX_PORT')
DATABASE = os.getenv('INFLUX_DATABASE')

def write_to_influxdb(client):
    """Weather API function to fetch data and update database. This uses
    norwegian open weather API from yr.no

    Args:
        client (InfluxDBClient): Database client

    Raises:
        sys.exit: RequestException
    """
    try:
        r = requests.get(URL, headers=headers, params=params, timeout=2)
        if r.status_code == 200:
            json_data = r.json()

            json_body = [
                {
                    'measurement': 'weather_measurements',
                    'tags': {
                        'meteringPoint': 'fmi-101065'
                    },
                    'fields': {'valueAsDouble': json_data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']}
                }
            ]
            client.write_points(json_body)
            logging.info(f'Weather status ok: {json_body}')
            client.close()
    except requests.exceptions.RequestException as e:
        logging.exception(e)
        raise sys.exit(f'Weather API request failed with {e}')

if __name__ == "__main__":
    client = InfluxDBClient(host=HOST, port=PORT, database=DATABASE)
    sys.exit(write_to_influxdb(client))
        