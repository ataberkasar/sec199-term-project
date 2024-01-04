from argparse import ArgumentParser
from utils import *

parser = ArgumentParser()

parser.add_argument('username', help='Twitter username.', type=str)
parser.add_argument('-s', '--since', help='Tweet scrape time limit. Defaults to \'1d\'. Hours, days, weeks, and months can be used.', 
                    type=str, default='1d')
parser.add_argument('-f', '--frpp', help='Frame Rate per Prompt for Deforum. Defaults to 10.', 
                    type=int, default=10)

args = parser.parse_args()
for k, v in vars(args).items():
    print(f'{k}:\t\t{v}')

scrape_tweets(args.username, args.since)
json_to_txt(os.path.join('scraper', 'jsons', f'{args.username}_output.json'))
llm_prompt_generator()

print(colored('\n\nWaiting for llm_outputs.txt', 'green'))
input('PRESS ENTER TO CONTINUE AFTER llm_outputs.txt UPDATED ')

deforum_prompt_generator(args.frpp)
