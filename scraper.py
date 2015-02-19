import praw
from HeatMap import HeatMap

user = praw.Reddit(
    user_agent='This bot will scan popular sub-reddits for comments and will create a keyboard heat map of the comment')

default_subreddits = ['pics', 'adviceanimals', 'dataisbeautiful', 'learnprogramming', 'acmuncg']
default_max = 3

subreddits = list(input('Enter subreddits you want to scrape, separate with spaces: ').split(' '))
print(subreddits)
if len(subreddits) == 1 and subreddits[0] == '':
    subreddits = default_subreddits
    print('We will search ' + str(subreddits) + ' by default')

try:
    max_comments = int(input('Enter number of comments you want to make a heat map of per subreddit: '))
except ValueError:
    max_comments = default_max
    print('By default, I will search ' + str(max_comments) + ' comments')

directory = input('Enter directory you want store the images in, make sure it exists: ')

heat = HeatMap(directory)

print('starting search')
for sub in subreddits:
    comments = user.get_comments(sub)
    print('\t\tin ' + sub)

    # we only get the amount of comments we want
    amount = max_comments
    for comment in comments:
        # nothing to map
        if len(comment.body) < 1:
            continue
        print(heat.get_heat_map(comment.body, comment.body[:(8 if len(comment.body) > 8 else len(comment.body))]))
        print(comment.body + '\n')

        # make sure the image is cleared
        heat.reset()
        amount -= 1
        if amount <= 0:
            break