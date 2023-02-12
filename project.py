#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance==0.2.11')
get_ipython().system('pip install beautifulsoup4==4.11.2')


# In[20]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ## Define Graphing Function

# In[22]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1 - Extracting Tesla Stock Data Using yfinance 

# In[23]:


Tesla = yf.Ticker('TSLA')


# In[24]:


tesla_data = Tesla.history(period = "max")


# In[25]:


tesla_data.reset_index(inplace = True)
tesla_data.head()


# In[7]:


tsla_data.reset_index(inplace=True)
tsla_data.head()


# ## Question 2 - Extracting Tesla Revenue Data Using Webscraping 

# In[26]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[27]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[28]:


tesla_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)


# In[29]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[30]:


tesla_revenue.tail()


# ## Question 3 - Extracting GameStop Stock Data Using yfinance

# In[31]:


GameStop = yf.Ticker("GME")


# In[32]:


gme_data = GameStop.history(period = 'max')


# In[33]:


gme_data.reset_index(inplace = True)
gme_data.head()


# ## Question 4 - Extracting GameStop Revenue Data Using Webscraping 

# In[34]:


url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text


# In[35]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[36]:


gme_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)


# In[37]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph

# In[38]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# ## Question 6: Plot GameStop Stock Graph

# In[39]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




