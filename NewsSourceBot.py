"""Fetches post data from Reddit /r/news subreddit between 1/1/2017 and 7/1/2017 then displays a bar graph of direct link sources versus frequency

PRAW library is used to interface the Reddit API and fetch post information from /r/news between the specified dates.
Post information is collected in redditGrabNews.txt file. The file is then parsed to count number of submissions
to each external url. countOfNewSource.csv file is created with external url information and frequency. The csv file is
then read and data is used to generate a bar graph using the Seaborn and Pandas library.

How to use:
- Seaborn and Pandas library required
- Edit praw.ini file and include your Reddit login information
- Run this script from console

File Name: NewsSourceBot.py
Author: Shuen Yasui
Date created: 7/30/2017
Last Modified: 8/20/2017]
Python Version: 3.6
"""

import praw
import time
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

r = praw.Reddit('myRedditLogin')
r.read_only = True
urls = {}
print("Logging in...")
def newsBot():
    """Uses PRAW to fetch reddit posts from /r/news

    This function will generate a .txt file with submission score, author name, link url 
    submitted to /r/news between the hard coded dates
    """
    print("Fetching posts from Reddit")
    f = open('redditGrabNews.txt', 'w', encoding="utf-8")
    for submission in r.subreddit("news").submissions(1483228800,1501545600):
        f.write(str(submission.score))
        f.write(";")
        f.write(submission.author.name)
        f.write(";")
        f.write(submission.url)
        f.write("\n")
    f.close()
def parseNewsData():
    """Opens redditGrabNews.txt file, parses the url and counts frequency and creates a .csv file.
    """
    print("Parsing post data")
    f = open("redditGrabNews.txt", 'r')
    g = open("countOfNewSource.csv", 'w', encoding="utf-8")
    lines = f.readlines()
    urlCount = []
    f.close()
    g.write('"News Source","Count"')
    g.write("\n")
    for line in lines:
        pos1 = line.find(";", 0)
        pos2 = line.find(";", pos1+1)
        pos3 = line.find("://", pos2)
        pos4 = line.find("://www.", pos2)
        pos5 = 0
        if pos4 > -1:
            pos5 = pos4 + 7
        else:
            pos4 = pos3
            pos5 = pos3 + 3
        pos6 = line.find("/", pos5)
        thisUrl = line[pos5:pos6] 
        if(thisUrl in urls):
            urls[thisUrl] += 1
        else:
            urls[thisUrl] = 1
    for url in urls:
        g.write(url)
        g.write(",")
        g.write(str(urls[url]))
        g.write("\n")
# newsBot() and parseNewsData() may be commented out if csv file already exists.
newsBot()
parseNewsData()
x2 = pd.read_csv("countOfNewSource.csv")
df = pd.DataFrame(x2)
df = df.sort_values(["Count"], ascending=False)
df.drop(df.index[40:], inplace=True)
sns.set(font_scale=0.9)
sns.set_style("white")
sns.barplot(x="Count", y="News Source", data=df, palette=sns.cubehelix_palette(40, start=.5, rot=-.75, reverse=True)).set_title("Top 40 sources from posts on /r/news \n between January 2017 and July 2017")
sns.despine()
plt.show()