## !/usr/local/bin/python

from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from commonutils import log_error
from uscis_cases import file_data
import csv
from datetime import datetime
import time
import re


def get_receipt_status(receipt_num: str):
  """
  Returns the case status for the given receipt number.
  """
  name = find_key(receipt_num, data)
      
  req_header = {'Host': 'egov.uscis.gov',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://egov.uscis.gov/casestatus/landing.do',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '69',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1'}
  req_params = {'changeLocale': '',
                'appReceiptNum': receipt_num,
                'initCaseSearch': 'CHECK+STATUS'}
  url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
  raw_html = simple_post(url, req_params, req_header)
  doc = BeautifulSoup(raw_html, 'html.parser')
  case_status = doc.find('div', {'class': 'rows text-center'}).find('h1').text
  case_details = doc.find('div', {'class': 'text-center'}).find('p').text
    # Extract the form number from the case details using regular expressions
    # form_number_match =re.search(r'Form [A-Z]{1}-[0-9]{3}', case_details)
  form_number_match =re.search(r'[A-Z]{1}-[0-9]{3}', case_details)
  if form_number_match:
      form_number = form_number_match.group()
  else:
      form_number = ''
#   return raw_to_status(doc.find_all('h1'))
  return [name, receipt_num, form_number, case_status, case_details]


def simple_post(url: str, params: dict[str, str], header: dict[str, str]):
  """
  Attempts to get the content at `url` by making an HTTP POST request.
  If the content-type of response is some kind of HTML/XML, return the
  text content, otherwise return None.
  """
  try:
    resp = post(url, data=params, headers=header)
    with closing(resp):
      if is_good_response(resp):
        return resp.content
      else:
        return None
  except RequestException as e:
    log_error('Error during requests to {0} : {1}'.format(url, str(e)))
    return None

def is_good_response(resp) -> bool:
  """
  Returns True if the response seems to be HTML, False otherwise.
  """
  content_type = resp.headers['Content-Type'].lower()
  return (resp.status_code == 200
          and content_type is not None
          and content_type.find('html') > -1)

def raw_to_status(headers):
  """
  Takes in a list of headers from the result HTML and returns an enum
  indicating the case status.
  TODO: Improve parsing and handle more cases
  """
  for header in headers:
    return header.text
  return None 

# ================================================================================
# ================================================================================
# ================================================================================
if __name__ == "__main__":
  s_date = datetime.today().strftime('%Y-%m-%d')
  case_numbers = []
  data = file_data()

  for key, values in data:
      for x in values:
        case_numbers.append(x)
  # print(case_numbers)   
  
  # Replace the values in the list with your actual case numbers
  def find_key(case_number, data):
      for key, values in data:
          if case_number in values:
              return key
      return None


  # Create a list to store the results
  results = []

  # Loop through each case number and pull the case status
  for case_number in case_numbers:
      # Append the results to the list
      results.append(get_receipt_status(case_number))
      print('Complete: '+ case_number)
      print("================================")
      time.sleep(0.5)


  # Write the results to a CSV file
  with open('case_status_'+s_date+'.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(['Name','Case Number', 'Form number', 'Case Status', 'Case Details'])
      for result in results:
          writer.writerow(result)
