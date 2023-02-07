from newsapi import NewsApiClient
from decouple import config
import sys

print(sys.path)

# Init
newsapi = NewsApiClient(api_key=config('NEWS_API_KEY'))

# fetch all articles that fall within the constraints
all_articles = newsapi.get_everything(
                                      q='personal finance',
                                      language='en',
                                      sort_by='relevancy',  
                                      )

  
