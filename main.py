import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path


def is_bitlink(url,token):
  
  parsed_url = urlparse(url)

  check_url = f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.netloc}{parsed_url.path}'

  headers = {
    "Authorization": token
  }

  link_type = requests.get(check_url, headers=headers)
  
  return link_type.ok


def shorten_link(token, user_url):
  
  url = 'https://api-ssl.bitly.com/v4/shorten/'

  headers = {
    "Authorization": token
  }

  params = {
    "long_url" : user_url
  }

  response = requests.post(url, headers = headers, json = params)
  response.raise_for_status()
  response_body = response.json()
  bitlink = response_body['link']
  
  return bitlink

def count_clicks(token, user_bitlink):
  
  metrics_url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_bitlink}/clicks/summary'

  headers = {
    "Authorization": token
  }

  metrics_params = {
    "unit" : "",
    "units" : "",
    "size" : "",
    "unit_reference": "",
  }

  response = requests.get(metrics_url, headers = headers, params = metrics_params)
  response.raise_for_status()
  all_clicks = response.json()['total_clicks']

  return all_clicks

if __name__ == '__main__':

  env_path = Path('.') / '.env'
  load_dotenv(dotenv_path=env_path)
  
  auth_token = os.environ['BITLY_TOKEN_AUTH']
  cmd_parser = argparse.ArgumentParser()
  cmd_parser.add_argument('link')
  user_url = cmd_parser.parse_args()
  
  if is_bitlink(user_url.link, auth_token):
    parsed_bitlink = urlparse(user_url.link)
    bitlink_address = f'{parsed_bitlink.netloc}{parsed_bitlink.path}'
    print('Всего кликов: ', count_clicks(auth_token, bitlink_address))
  else:
    try:
      new_bitlink = shorten_link(auth_token, user_url.link)
      print('Битлинк', new_bitlink)
    except requests.exceptions.HTTPError:
      print("Данная ссылка не существует")
  