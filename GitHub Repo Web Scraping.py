#!/usr/bin/env python
# coding: utf-8

# # Top Repos for GitHub Topics
# 
# 

# 

# ## Pick a website and describe your objective
# - Browse through different sites and pick on to scrape
# - Identify the info you'd like to scrape from the site, decide format for output CSV file
# - Summarize project idea

# ## Project Outline
# - We're going to scrape https://github.com/topics
# - We'll get a list of topics, for each topic we'll get topic title, topic page URL and description
# - For each topic, we'll get the top 25 repos from the topic page
# - For each repo, we'll grab the name, username, stars and repo URL
# - For each topic, we'll create a CSV file in the following format:
# '''
# Repo Name, Username, Stars, Repo URL
# '''
# 
# 

# ### Use the requests library to download web pages

# In[1]:


get_ipython().system('pip install requests --upgrade --quiet')


# In[2]:


import requests


# In[3]:


topics_url = "https://github.com/topics"


# In[4]:


response = requests.get(topics_url)


# In[5]:


response.status_code


# In[6]:


page_contents = response.text


# In[7]:


page_contents[:1000]


# In[8]:


with open('weboage.html', 'w') as f:
    f.write(page_contents)


# In[ ]:





# ### Use BeautifulSoup to parse and extract info

# In[9]:


get_ipython().system('pip install beautifulsoup4 --upgrade --quiet')


# In[10]:


from bs4 import BeautifulSoup


# In[11]:


doc = BeautifulSoup(page_contents, 'html.parser')


# In[19]:


selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_title_tags = doc.find_all('p',
                     {'class': selection_class })


# In[20]:


len(topic_title_tags)


# In[21]:


topic_title_tags


# In[24]:


topic_description_class = 'f5 color-fg-muted mb-0 mt-1'
topic_description_tags = doc.find_all('p', {'class': topic_description_class})


# In[25]:


len(topic_description_tags)


# In[26]:


topic_description_tags


# In[29]:


topic_title_tag0 = topic_title_tags[0]


# In[30]:


div_tag = topic_title_tag0.parent


# In[31]:


div_tag


# In[32]:


topic_link_tags = doc.find_all('a',
                               {'class': 'no-underline flex-1 d-flex flex-column'})


# In[33]:


len(topic_link_tags)


# In[36]:


topic_0_url = "https://github.com" + topic_link_tags[0]['href']
print(topic_0_url)


# In[43]:


topic_titles= []

for tag in topic_title_tags:
    topic_titles.append(tag.text)
print(topic_titles)


# In[46]:


topic_descriptions = []

for tag in topic_description_tags:
    topic_descriptions.append(tag.text.strip())
print(topic_descriptions)


# In[51]:


topic_urls = []
base_url = 'https://github.com'
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])
    
topic_urls


# In[52]:


get_ipython().system(' pip install pandas --quiet')


# In[54]:


import pandas as pd


# In[59]:


topics_dict = {
    'Title': topic_titles,
    'Description': topic_descriptions,
    'URL': topic_urls
}


# In[ ]:





# In[60]:


topics_df = pd.DataFrame(topics_dict)


# In[61]:


topics_df


# ## Create CSV files with the extracted information

# In[63]:


topics_df.to_csv('topics.csv', index = None)


# ## Getting information out of a topic page

# In[64]:


topic_page_url = topic_urls[0]


# In[65]:


topic_page_url


# In[66]:


response = requests.get(topic_page_url)
response.status_code


# In[128]:


topic_doc = BeautifulSoup(response.text, 'html.parser')


# In[129]:


topic_doc


# #### as the username and repo name are contained in 2 seperate a tags within the same h3, we select the h3 class

# In[130]:


h3_selection_class = "f3 color-fg-muted text-normal lh-condensed"
repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})


# In[131]:


len(repo_tags)


# #### a_tags[0] gives us the username, a_tags[1] gives us the repo name

# In[132]:


a_tags = repo_tags[0].find_all('a')
a_tags[0].text.strip()


# In[133]:


a_tags[1].text.strip()


# In[134]:


repo_url = base_url + a_tags[1]['href']
repo_url


# #### Could not figure out how to add number of stars, incorrect referral

# In[142]:


def get_repo_info(h3_tag):
    # returns required info about repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    return username, repo_name, repo_url


# In[143]:


get_repo_info(repo_tags[0])


# In[148]:


topics_repos_dict = {
    'Username': [],
    'Repository Name': [],
    'Repository Link': []
}

for i in range(len(repo_tags)):
    repo_info = get_repo_info(repo_tags[i])
    topics_repos_dict['Username'].append(repo_info[0])
    topics_repos_dict['Repository Name'].append(repo_info[1])
    topics_repos_dict['Repository Link'].append(repo_info[2])


# In[150]:


topics_repos_dict


# In[153]:


topics_repos_df = pd.DataFrame(topics_repos_dict, index = None)
topics_repos_df


# In[186]:


def get_topic_page(topic_url):
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def get_repo_info(h3_tag):
    # returns required info about repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    return username, repo_name, repo_url
    
    
def get_topic_repos(topic_page_url):
    
    h3_selection_class = "f3 color-fg-muted text-normal lh-condensed"
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
    topics_repos_dict = {
        'Username': [],
        'Repository Name': [],
        'Repository Link': []
    }

    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i])
        topics_repos_dict['Username'].append(repo_info[0])
        topics_repos_dict['Repository Name'].append(repo_info[1])
        topics_repos_dict['Repository Link'].append(repo_info[2])
        
    return pd.DataFrame(topics_repos_dict)


# In[187]:


url5 = topic_urls[5]
url5


# In[188]:


topic5_doc = get_topic_page(url5)
topic5_doc


# In[189]:


topic5_repos = get_topic_repos(topic5_doc)


# In[190]:


topic5_repos


# In[ ]:




