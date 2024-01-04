import os
import re
import json
import requests
import traceback
import subprocess
from datetime import datetime
from termcolor import colored

def scrape_tweets(username, _from):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    scraper_dir = os.path.join(base_dir, 'scraper')

    crawl_command = [
        'scrapy', 'crawl', 'NitterSpider',
        '-a', f'username={username}',
        '-a', f'_from={_from}',
        '-O', f'jsons/{username}_output.json'
    ]
    
    download_command = [
        'scrapy', 'crawl', 'ImageSpider',
        '-a', f'username={username}'
    ]

    try:
        subprocess.run(crawl_command, check=True, cwd=scraper_dir, shell=False)
    except subprocess.CalledProcessError as e:
        error_traceback = traceback.format_exc()
        print(colored('[ERROR]', 'red'), e)
        print(colored(error_traceback, 'yellow'))
        print(f'Error encountered during execution of the command\n{" ".join(crawl_command)}')
        
    try:
        subprocess.run(download_command, check=True, cwd=scraper_dir, shell=False)
    except subprocess.CalledProcessError as e:
        error_traceback = traceback.format_exc()
        print(colored('[ERROR]', 'red'), e)
        print(colored(error_traceback, 'yellow'))
        print(f'Error encountered during execution of the command\n{" ".join(download_command)}')

# Preprocessor should be implemented for specific use case
# An example implementation can be seen below
def tweet_preprocessor(tweet):
    tweet['tweet'] = re.sub(r'\s+', ' ', tweet['tweet'])
    tweet['tweet'] = '' if tweet['tweet'].startswith('//') else tweet['tweet'].split(' — ')[0].replace('“', '').replace('”', '')
    
    return tweet
    
def json_to_txt(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        tweets = json.load(file)

    tweets.sort(key=lambda x: datetime.strptime(x['tweet_date'], '%Y-%m-%d %H:%M:%S'))
    
    grouped_tweets = {}
    for tweet in tweets:
        date_parts = tweet['tweet_date'].split()[0].split('-')
        year, month, day = date_parts

        if year not in grouped_tweets:
            grouped_tweets[year] = {}
        if month not in grouped_tweets[year]:
            grouped_tweets[year][month] = {}
        if day not in grouped_tweets[year][month]:
            grouped_tweets[year][month][day] = []
        grouped_tweets[year][month][day].append(tweet)

    with open('output.txt', 'w+', encoding='utf-8') as f:
        for year, months in grouped_tweets.items():
            for month, days in months.items():
                for day, tweets_in_day in days.items():
                    counter = 1
                    for tweet in tweets_in_day:
                        f.write(f'{counter}. ')
                        tweet = tweet_preprocessor(tweet)
                        f.write(tweet['tweet'])
                        counter += 1
                        f.write('\n')
                    f.write('\n')
                f.write('\n')

def llm_prompt_generator():
    with open('llm_prompts.txt', 'w+', encoding='utf-8') as prompt_file:
        prompt_file.write("""
Your job is to create descriptive sentences using keywords in the given tweets. Make sure your sentences are easy to visualize and can be turned into a painting. 

# Rules
* I will give you a base sentence, that should help you to have an idea, and list of tweets that you should get keywords
* If you want, you can change keywords, but ideas must be intact
* Base sentence can be omitted by the user (me)
* Generated sentence should be simple and short, 8 words at most, ie. a kid can easily understand
* Sentence should be in english, so if tweets from any other language comes you need to translate 
* Generated sentence should contain one keyword from each tweet
* Sentence should be descriptive, and easy to visualize, since it will be used to create a painting

# Input Format
Sentence: Base sentence
Tweets: 
1. Tweet-1
2. Tweet-2
3. Tweet-3

# Output Format
Keywords-1: Tweet-1-keywords
Keywords-2: Tweet-2-keywords
Keywords-3: Tweet-3-keywords
Sentence: 
Generated single sentence with at least one keyword from each tweet

****************************************************\n""")
        with open('output.txt', 'r', encoding='utf-8') as tweet_file:
            sentence_counter = 0
            for line in tweet_file:
                if (sentence_counter == 0):
                    prompt_file.write('Sentence:\nTweets:\n')
                if (line != '\n'):
                    prompt_file.write(line)
                    sentence_counter += 1
                else:
                    sentence_counter = 0
                    prompt_file.write("\n\n")
        
        os.remove('output.txt')

def deforum_prompt_generator(frame_per_line):
    counter = 0
    prompts = {}
    with open('llm_outputs.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if (line[0] == '#'):
                continue
            if (line == '\n'):
                continue
            
            prompts[f'{counter}'] = line.strip()
            counter += frame_per_line
    with open('deforum_prompts.txt', 'w+') as f:
        f.write(json.dumps(prompts, indent=4))
        f.write('\n\n')
        f.write('Max Frame: ' + str(counter))

