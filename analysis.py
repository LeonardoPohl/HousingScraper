import pandas as pd
import time
import urllib
import re
import os

from providers import ParariusProvider
from utils import Entry
import webbrowser

import pickle

import smtplib, ssl

from pretty_html_table import build_table

urls = {
  'Pararius Den Haag':  "/apartments/den-haag/0-1750/2-bedrooms",
  'Pararius Leidschendam': "/apartments/leidschendam/0-1750/2-bedrooms",
  'Pararius Rijswijk': "/apartments/rijswijk/0-1750/2-bedrooms",
  'Pararius Leiden': "/apartments/leiden/0-1750/2-bedrooms",
  'Pararius Wassenaar': "/apartments/Wassenaar/0-1750/2-bedrooms",
 # 'Pararius Utrecht': "/apartments/utrecht/0-1750/2-bedrooms",
  'Pararius Leidedorp': "/apartments/leiderdorp/0-1750/2-bedrooms",
  'Pararius Oegstgeest': "/apartments/oegstgeest/0-1750/2-bedrooms",
  'Pararius Rijnsburg': "/apartments/rijnsburg/0-1750/2-bedrooms",
 # 'Pararius Delft': "/apartments/delft/0-1750/2-bedrooms",
  'Pararius Voorburg': "/apartments/voorburg/0-1750/2-bedrooms"
}

# Too good to be true threshold (probably fake listing)
tgtbt_area_price_threshold = 5
# Tiny Room Threshold (the rooms are just too small)
tiny_room_threshold = 15

output_file_name = "output.dat"

def get_entries():
  pps = [ParariusProvider(urls[url], url.removeprefix('Pararius ')) for url in urls]
       
  for pp in pps[::-1]:
    pp.query_entries()
    pp.get_detailed_results()
    break
  
  entries = []
  for pp in pps:
    entries += pp.entries

  df = pd.DataFrame(entries)
  return df

def filter_entries(df):
  df['Price per area'] = df['price'] / df['area']
  df['Price per room'] = df['price'] / df['rooms']
  df['Area per room'] = df['area'] / df['rooms']

  initial_rows = df.shape[0]

  df = df[df['Price per area'] > tgtbt_area_price_threshold]
  df = df[df['Area per room'] > tiny_room_threshold]
  df = df[~df["description"].str.contains('permit', case=False)]
  df = df[df["rented"].isnull()]

  print(f"{df.shape[0]}/{initial_rows} rows eligible")

def filter_existing_entries(df):
  array = []

  if os.path.isfile(output_file_name):
    with open(output_file_name, "r") as f:
      array = f.read()[1:-1].replace("'","").strip().split(', ')
      df2 = df[~df["link"].isin(array)]
      print(f"{df2.shape[0]} new Properties!")
    
  with open(output_file_name, "w") as f:
    array += list(df2["link"])
    f.write(str(array))

  df2.head()
  return df2

def df_to_email(df):
  df2 = df.copy()
  df2['link'] = df['link'].apply(lambda k: f'<a href="{k}">{k}</a>')
  df2['description'] = df['description'].apply(lambda k: k.replace('\n', '<br>'))
  df2['address'] = df['address'].apply(lambda k: Address.to_string(k).replace('\n', '<br>'))

  html = f"""\
  <html>
    <head>
      <style>
        {0}
      </style>
    </head>
    <body>
      Hi Maria and Leo,

      I have found the following new Appartements. Have fun looking at them :)

      {build_table(df2, 'blue_light')}
    </body>
  </html>
  """

  return html


def send_entries_email(df):
  port = 465  # For SSL
  password = 'xrko gsmg xivc oshm'

  # Create a secure SSL context
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("xbipho.sender@gmail.com", password)
    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = f'I found {len(links)} new Appartements!'
    msg['From'] = 'xbipho.sender@gmail.com'
    msg['To'] = 'pohly3@gmail.com'

    msg.set_content(df_to_email(df))

    server.send_message(msg)

if __name__=='__main__':
  df = get_entries()
  filter_entries(df)
  df2 = filter_existing_entries(df)

  if df2:
    df_to_email


# %%
links = list(df2.link)
for link in links:
  webbrowser.open_new_tab(link)

# %%


# %%
my_style = """background-color: rgba(0, 0, 0, 0);
border-bottom-color: rgb(0, 0, 0);
border-bottom-style: none;
border-bottom-width: 0px;
border-collapse: collapse;
border-image-outset: 0px;
border-image-repeat: stretch;
border-image-slice: 100%;
border-image-source: none;
border-image-width: 1;
border-left-color: rgb(0, 0, 0);
border-left-style: none;
border-left-width: 0px;
border-right-color: rgb(0, 0, 0);
border-right-style: none;
border-right-width: 0px;
border-top-color: rgb(0, 0, 0);
border-top-style: none;
border-top-width: 0px;
box-sizing: border-box;
color: rgb(0, 0, 0);
display: table;
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-size: 12px;
height: 1675px;
line-height: 20px;
margin-left: 0px;
margin-right: 0px;
margin-top: 12px;
table-layout: fixed;
text-size-adjust: 100%;
width: 700px;
-webkit-border-horizontal-spacing: 0px;
-webkit-border-vertical-spacing: 0px;
-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"""


# %%
def HTML_with_style(df, style=None, random_id=None):
    from IPython.display import HTML
    import numpy as np
    import re

    df_html = df.to_html()

    if random_id is None:
        random_id = 'id%d' % np.random.choice(np.arange(1000000))

    if style is None:
        style = """
        <style>
            table#{random_id} {{color: blue}}
        </style>
        """.format(random_id=random_id)
    else:
        new_style = []
        s = re.sub(r'</?style>', '', style).strip()
        for line in s.split('\n'):
                line = line.strip()
                if not re.match(r'^table', line):
                    line = re.sub(r'^', 'table ', line)
                new_style.append(line)
        new_style = ['<style>'] + new_style + ['</style>']

        style = re.sub(r'table(#\S+)?', 'table#%s' % random_id, '\n'.join(new_style))

    df_html = re.sub(r'<table', r'<table id=%s ' % random_id, df_html)

    return HTML(style + df_html)

# %%
from utils import Address
df['address'].apply(lambda k: Address.to_string(k).replace('\n', '<br>'))

# %%


# %%
# df.to_html('html.html', 
#            formatters = {'link': lambda k: f'<a href="{k}">{k}</a>',
#                          'description': lambda k: k.replace('\n', '<br>')}, 
#            escape=False,
#            index=False)
df3 = df.copy()
df3['link'] = df['link'].apply(lambda k: f'<a href="{k}">{k}</a>')
df3['description'] = df['description'].apply(lambda k: k.replace('\n', '<br>'))
df3['address'] = df['address'].apply(lambda k: Address.to_string(k).replace('\n', '<br>'))
html = HTML_with_style(df3, '<style>table {{{}}}</style>'.format(my_style))

with open('html.html', 'w') as f:
  f.write(str(html))

# %%
if links:
  port = 465  # For SSL
  password = 'xrko gsmg xivc oshm'

  # Create a secure SSL context
  context = ssl.create_default_context()

  with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("xbipho.sender@gmail.com", password)
    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = f'I found {len(links)} new Appartements!'
    msg['From'] = 'xbipho.sender@gmail.com'
    msg['To'] = 'pohly3@gmail.com'

    df3 = df.copy()
    df3['link'] = df['link'].apply(lambda k: f'<a href="{k}">{k}</a>')
    df3['description'] = df['description'].apply(lambda k: k.replace('\n', '<br>'))
    df3['address'] = df['address'].apply(lambda k: Address.to_string(k).replace('\n', '<br>'))
    html = HTML_with_style(df3, '<style>table {{{}}}</style>'.format(my_style))
    
    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server.send_message(msg)