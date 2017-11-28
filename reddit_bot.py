import praw
import time
import os

REPLY_MESSAGE = ('I also love Spider-Man! [Here](https://i.redd.it/rhtxxcwpsq001.png) is an image!')


def authenticate():
    print ('Authenticating..')
    reddit = praw.Reddit('spideyfactbot', user_agent='Spiderman_Fact_Bot responder')
    print ('Authenticated as {}'.format(reddit.user.me()))
    return reddit


def main():
    reddit = authenticate()
    comments_replied_to = get_saved_comments()
    print (comments_replied_to)

    while True:
            run_bot(reddit, comments_replied_to)


def run_bot(reddit, comments_replied_to):
    print ('Obtaining 25 comments...')

    for comment in reddit.subreddit('test') .comments(limit=25):
      if '!Spideyfact' in comment.body and comment.id not in comments_replied_to and comment.author != reddit.user.me():
        print ('String with \'!Spideyfact\' found in comment ' + comment.id)
        comment.reply(REPLY_MESSAGE)
        print ('Replied to comment ' + comment.id)

        comments_replied_to.append(comment.id)

        with open ('comments_replied_to.txt', 'a') as f:
            f.write(comment.id + '\n')


    print ('Sleeping for 10 minutes...')
    # Sleep for 600 seconds... Which is 10 minutes.
    time.sleep(10)

def get_saved_comments():
	if not os.path.isfile('comments_replied_to.txt'):
		comments_replied_to = []
	else:
		  with open('comments_replied_to.txt', 'r') as f:
			     comments_replied_to = f.read()
			     comments_replied_to = comments_replied_to.split('\n')
           # comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to

if __name__ == '__main__':
  main()
