import praw
import config
import time
import urllib.request, urllib.parse, urllib.error
import os

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "u/-WarHounds-'s anti product spam hunting bot that replies on comments by spammers to save innocent redditors from scams")
	print("Logged in!")

	return r

def comments_rep_to():
    with open ("comments_replied_to.txt", "a") as f:
        f.write(comment.id + "\n")

def checkop():
    url = ("https://api.pushshift.io/reddit/search/comment/?author=" + comment.submission.author.name)
    response = urllib2.urlopen(url)
    with open('output.txt', 'w') as shtt:
        shtt.write(response.read())

def checkingvotes():
    print("Checking votes.")

def run_bot(r, comments_replied_to):
	print("Searching last 1,000 comments")

	for comment in r.subreddit('popular+mechanical_gifs+Damnthatsinteresting+test+DesignPorn+DidntKnowIWantedThat+Eyebleach+Perfectfit+Unexpected+aww+blackmagicfuckery+funny+geek+gifs+gifsthatkeepongiving+holdmybeer+interestingasfuck+oddlysatisfying+pics+videos+woahdude+combinedgifs+beamazed+nextfuckinglevel+wholesomegifs+noisygifs+ofcoursethatsathing+productporn+holdmycatnip+bettereveryloop+gifsthatendtoosoon+holdmycosmo+geek+yesyesyesno+yesyesyesyesno').comments(limit=1000):
		if "/u/BotDetective test" in comment.body and comment.id not in comments_replied_to and comment.author or "etrendan.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "geekydeal.store/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "pearlgadget.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "stiflingdeals.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "prenkart.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "kickize.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "hashtagssale.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
			print(("String with blacklisted link found in comment " + comment.id))
			comment.reply("**WARNING:** This is likely a fake account setup to promote the product shown in the video, please don't encourage this by either visiting the website or upvoting.\n\nThese bots are setup to steal unique comments from other users to pass as real people.\n\nIf you would like to help verify whether this user is a bot, you can check for duplicate comments using redditsearch.io\n\n**^If ^the ^user ^is ^indeed ^a ^bot, ^please ^report ^the ^message ^to ^the ^moderators, ^If ^you ^believe ^this ^was ^a ^mistake, [^send ^me ^a ^message!](https://www.reddit.com/message/compose/?to=-WarHounds-&subject=BotDetective - Error)**")
			print(("Replied to comment " + comment.id))

			comments_replied_to.append(comment.id)
			comments_rep_to()
			checkop()
        
	print("Search Completed.")

	get_karma()

	print(comments_replied_to)

	print("Sleeping for 60 seconds...")
	#Sleep for 10 seconds...
	time.sleep(60)

def get_karma():
    user = r.user.me()
    comment_list = []
    for comment in user.comments.new(limit=20):
        comment_list.append(comment.id)
    p_id = open("Parent_id.txt","a+")
    for comment in comment_list:
        comment = r.comment(id = comment)
        print(("Comment with " + str(comment.score) + " found"))
        if int(comment.score) < 0:
            print(("Comment with " + str(comment.score) + " found"))
            parent_id = comment.parent_id
            if parent_id not in p_id.read().split("\n"):
                parent_comment = r.comment(id=parent_id)
                body = comment.body
                comment.delete()
                parent_comment.reply(body)
                p_id.write(comment.parent_id + "\n")
                print("Comment reposted.")
        else:
            checkingvotes()

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = [_f for _f in comments_replied_to if _f]

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
	run_bot(r, comments_replied_to)
