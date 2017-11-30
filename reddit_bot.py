import os
import time
import random

import praw
import spidey_facts


def authenticate():
  print('Authenticating...')
  reddit = praw.Reddit('spideyfactbot', user_agent='Spiderman_Fact_Bot responder')
  print('Authenticated as', reddit.user.me())
  return reddit


def main():
  reddit = authenticate()
  comments_replied_to = get_saved_comments()
  print(comments_replied_to)

  while True:
    run_bot(reddit, comments_replied_to)


def get_reply():
  random.shuffle(spidey_facts.facts)
  return 'You requested a Spider-Man fact! Here it is:\n\n' + '>' + spidey_facts.facts[0] + '\n\n[Source code here!](https://github.com/TangJames/SpideyFact-Reddit-Bot)'


def run_bot(reddit, comments_replied_to):
  print('Obtaining 25 comments...')

  for comment in reddit.subreddit('Spiderman').comments(limit=25):
    if '!Spideyfact' in comment.body and comment.id not in comments_replied_to and comment.author != reddit.user.me():
      print('String with \'!Spideyfact\' found in comment ' + comment.id)
      comment.reply(get_reply())
      print('Replied to comment ' + comment.id)

      comments_replied_to.append(comment.id)

      with open('comments_replied_to.txt', 'a') as f:
          f.write(comment.id + '\n')


  print('Sleeping for 10 seconds...')
  # Sleep for 10 seconds...
  time.sleep(10)


def get_saved_comments():
  if not os.path.isfile('comments_replied_to.txt'):
    comments_replied_to = []
  else:
    with open('comments_replied_to.txt', 'r') as f:
      comments_replied_to = f.read()
      comments_replied_to = comments_replied_to.split('\n')


  return comments_replied_to

if __name__ == '__main__':
  main()
