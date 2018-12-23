import praw
import config
import time
import urllib.request, urllib.parse, urllib.error
import os
import requests

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "u/-WarHounds-'s anti product spam hunting bot that replies on comments by spammers to save innocent redditors from scams")
	print("Logged in!")

	return r

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = [_f for _f in comments_replied_to if _f]
    return comments_replied_to

def run_bot(r, comments_replied_to):

    subredditstosearch = r.subreddit('thriftstorehauls+crappyoffbrands+popular+mechanical_gifs+Damnthatsinteresting+DesignPorn+DidntKnowIWantedThat+Eyebleach+Perfectfit+Unexpected+aww+blackmagicfuckery+funny+geek+gifsthatkeepongiving+holdmybeer+interestingasfuck+oddlysatisfying+pics+videos+woahdude+combinedgifs+beamazed+nextfuckinglevel+wholesomegifs+noisygifs+ofcoursethatsathing+productporn+holdmycatnip+bettereveryloop+gifsthatendtoosoon+holdmycosmo+geek+yesyesyesno+yesyesyesyesno+all').comments(limit=5000)
    subredditsthatdontallowcomments = r.subreddit('gifs+test').comments(limit=1000)
    urlshorteners = r.subreddit('finalfantasy+crappyoffbrands+didntknowiwantedthat+designporn+ComedyCemetery+nhl+donaldglover+rickandmorty+thriftstorehauls+Undertale+PandR+Dundermifflin+beatles+Boruto+DanLeBatardShow+thesimpsons+justneckbeardthings+the_donald+DavidBowie+gameofthrones+ddlc+xxxtentacion+therewasanattempt+woahdude+pics+batman+funny+breakingbad+supremeclothing+memes+thriftstorehauls+crappyoffbrands+popular+mechanical_gifs+Damnthatsinteresting+DesignPorn+DidntKnowIWantedThat+Eyebleach+funny+geek+interestingasfuck+oddlysatisfying+pics+videos+woahdude+combinedgifs+beamazed+nextfuckinglevel+wholesomegifs+noisygifs+ofcoursethatsathing+productporn').comments(limit=4000)
    comment_list = []

    def extractlink():
        with open('extractlink.txt', 'r') as g:
            contents = g.read()
            try:
                req = urllib.request.Request(g.read())
                res = urllib.request.urlopen(req)
                finalurl = res.geturl()
                print(("Links to " + finalurl))
                if "qualifiedfashion" or "newtshirtshop" or "gearshop" or "QualifiedFashi" or "usagearshop" or "tee" or "shirt" or "gear" or "bamboom" in finalurl:
                    print(("String with blacklisted link found in comment " + comment.id + "from " +  comment.author.name))
                    comment.reply("**WARNING:** This is likely a fake account setup to promote the product shown in this post, please don't encourage this by either visiting the website or any other links provided.\n\n**^If ^the ^user ^is ^indeed ^a ^bot, ^please ^report ^the ^message ^to ^the ^moderators, ^If ^you ^believe ^this ^was ^a ^mistake, ^have ^any ^other ^links ^you ^would ^like ^to ^report, ^or ^would ^like ^to ^add ^your ^subreddit, [^send ^me ^a ^message!](https://www.reddit.com/message/compose/?to=-WarHounds-&subject=BotDetective)**")
                    print(("Replied to comment " + comment.id))
                    with open ("comments_replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")
                else:
                    print("False-positive")
            except:
                print("False-positive")

    def get_karma():
        for comment in r.user.me().comments.new(limit=20):
            prevcomment = comment.body
            parent = comment.parent()
            score = comment.score
            with open("karmalist.txt", "r+") as karmalist:
                if comment.id not in karmalist.read().split("\n"):
                    karmalist.write(comment.id + "\n")
            with open("Parent_id.txt","r+") as p_id, open("karmalist.txt", "r+") as karmalist:
                if comment in karmalist.read().split("\n"):
                    if int(score) < 0:
                        print(("Comment with " + str(score) + " found"))
                        if parent in p_id.read().split("\n"):
                            print(parent + " found in parent_id.txt")
                            run1()
                        else:
                            parent.reply(prevcomment)
                            p_id.write(comment.parent_id + "\n")
                            print("Comment reposted.")
                            comment.delete
                            time.sleep(5)

    def part1():
        print(("String with blacklisted link found in comment " + comment.id + " by " +  comment.author.name))
        #comment.submission.report('Likely posted by a bot to promote product link.')
        #print(("Reported submission" + comment.submision.id))
        comment.report('This is likely posted by a bot to promote product link.')
        print(("Reported comment " + comment.id + "from " + comment.author.name))
        comments_replied_to.append(comment.id)
        with open ("comments_replied_to.txt", "a") as f, open ("check_if_op_is_bot.txt", "r+") as b:
            f.write(comment.id + "\n")
            b.write("https://api.pushshift.io/reddit/search/comment/?author=" + comment.submission.author.name + "\n")
            print("Wrote url to check_if_op_is_bot.txt")

    def run1():
        print("Searching last 1,000 comments in subreddits that don't allow comments...")
        for comment in subredditsthatdontallowcomments:
            if "geardate.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "gearshop.space" in comment.body and comment.id not in comments_replied_to and comment.author or "torridmart.com/products" in comment.body and comment.id not in comments_replied_to and comment.author or "apeirondeals.com/products" in comment.body and comment.id not in comments_replied_to and comment.author or "/products/creative-bottle-openers-tool-flying-cap-launcher" in comment.body and comment.id not in comments_replied_to and comment.author or "ref=cm_sw_r_cp_apa_i_7dIfCb0CW169G" in comment.body and comment.id not in comments_replied_to and comment.author or "/u/BotDetective test" in comment.body and comment.id not in comments_replied_to and comment.author or "etrendan.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "geekydeal.store/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "pearlgadget.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "stiflingdeals.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "prenkart.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "kickize.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "hashtagssale.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
                part1()
        print("Search Completed.")

    run1()

    def run2():

        def part2():
            print(("String with blacklisted link found in comment " + comment.id + " by " + comment.author.name))
            comment.reply("**WARNING:** This is likely a fake account setup to promote the product shown in the video, please don't encourage this by either visiting the website or any other links provided.\n\nThese bots are setup to steal unique comments from other users to pass as real people.\n\nIf you would like to help verify whether this user is a bot, you can check for duplicate comments using redditsearch.io\n\n**^If ^the ^user ^is ^indeed ^a ^bot, ^please ^report ^the ^message ^to ^the ^moderators, ^If ^you ^believe ^this ^was ^a ^mistake, [^send ^me ^a ^message!](https://www.reddit.com/message/compose/?to=-WarHounds-&subject=BotDetective - Error)**")
            comment.report('This is likely posted by a bot to promote product link.')
            comment.submission.report('This is likely posted by a bot to promote product link.')
            print(("Reported comment " + comment.id + "from " + comment.author.name))
            print(("Reported submission " + comment.submission.id + "from " + comment.submission.author.name))
            print(("Replied to comment " + comment.id))
            comments_replied_to.append(comment.id)
            with open ("comments_replied_to.txt", "a") as f, open ("check_if_op_is_bot.txt", "r+") as b:
                f.write(comment.id + "\n")
                b.write("https://api.pushshift.io/reddit/search/comment/?author=" + comment.submission.author.name + "\n")
                print("Wrote url to check_if_op_is_bot.txt")

        print("Searching last 5,000 comments in subreddits...")

        for comment in subredditstosearch:
            if comment.subreddit not in subredditsthatdontallowcomments:
                if "geardate.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "gearshop.space" in comment.body and comment.id not in comments_replied_to and comment.author or "torridmart.com/products" in comment.body and comment.id not in comments_replied_to and comment.author or "apeirondeals.com/products" in comment.body and comment.id not in comments_replied_to and comment.author or "/products/creative-bottle-openers-tool-flying-cap-launcher" in comment.body and comment.id not in comments_replied_to and comment.author or "ref=cm_sw_r_cp_apa_i_7dIfCb0CW169G" in comment.body and comment.id not in comments_replied_to and comment.author or "/u/BotDetective test" in comment.body and comment.id not in comments_replied_to and comment.author or "etrendan.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "geekydeal.store/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "pearlgadget.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "stiflingdeals.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "prenkart.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "kickize.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "hashtagssale.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
                    part2()
            else:
                run1()
                print("Comment found in a subreddit that doesn't allow comments")
        print("Search Completed.")

    run2()
    get_karma()

    def run3():
        print("Searching last 4,000 comments for url shorteners...")

        for comment in urlshorteners:
            if "goo.gl" in comment.body and comment.id not in comments_replied_to and comment.author or "bit.ly" in comment.body and comment.id not in comments_replied_to and comment.author or "sungearstore.com" in comment.body and comment.id not in comments_replied_to and comment.author or "baamboom.club" in comment.body and comment.id not in comments_replied_to and comment.author or "qualifiedfashion.com" in comment.body and comment.id not in comments_replied_to and comment.author or "usagearshop.com" in comment.body and comment.id not in comments_replied_to and comment.author or "newtshirtshop.com" in comment.body and comment.id not in comments_replied_to and comment.author or ".website" in comment.body and comment.id not in comments_replied_to and comment.author or ".icu" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
                print("Search Completed.")
                print(("String with possibly shortened link found in comment " + comment.id + " by " + comment.author.name))
                def part3():
                    with open ('findlink.txt', 'w') as findlink:
                        findlink.write(comment.body)
                        findlink.close()
                        print("findlink written and closed.")
                        getlink()

                part3()

        print("Searching last 1,000 comments")

    for comment in comment_list:
        comment = r.comment(id = comment)

    def getlink():
        with open('findlink.txt') as infile, open('extractlink.txt', 'w') as outfile:
            for line in infile:
                outfile.write(line[line.find("](")+2: line.find(")")])
                print("extractlink written.")
            infile.close()
            outfile.close()
            extractlink()

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
	run_bot(r, comments_replied_to)
