import pandas as pd
from bs4 import BeautifulSoup
from requests import request
from scrapper.PortionsStringParser import PortionString

class Scrapper:
  def __init__(
      self, 
      url = 'https://drapaolamongalo.com/grupos-de-alimentos-con-sus-porciones/',
      ):
    self.url = url
    self.parser = PortionString()


  def get_data_as_df(self):
    df = pd.DataFrame(self.get_processed_data())
    df = df.astype({
      'taza': 'float',
      'gramo': 'float',
      'oz': 'float',
      'unidad': 'float',
      'clara': 'float',
      'cda': 'float',
      'ml': 'float',
      'cdita': 'float'
    })
    return df

  
  def get_processed_data(self):
    data = []
    parsed_html = self.get_parsed_html(self.url)

    for title, table in parsed_html:
      table_data = self.clean_table_data(title, table)

      data += table_data
    
    return data


  def get_parsed_html(self, url):
    response = request('GET', url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table_titles = soup.find_all('h3')
    table_titles = [next(title.children) for title in table_titles]

    tables = soup.find_all('table')
    
    parsed_html = zip(table_titles, tables)
    
    return  parsed_html
  

  def clean_table_data(self, title, table_data):
    data = []
    headers = []
    first_row = True
    
    table_body = table_data.find('tbody').find_all('tr')
    
    for row in table_body:
      cols = row.find_all('td')
      col_num = 0
      item = {}

      for col in cols:
        if first_row:
          headers.append(next(col.find('strong').children))
          continue
        
        header = headers[col_num % 2]
        cell_value = col.text

        item[header] = cell_value

        if self.parser.validate_string(cell_value):
          decomposed_portions = self.parser.clean(cell_value)
          item.update(decomposed_portions)

        item['Grupo'] = title

        col_num += 1
      
      data.append(item)
      first_row = False
    return data[1:]
