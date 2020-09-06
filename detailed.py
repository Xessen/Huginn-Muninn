from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import praw
from time import sleep
from datetime import datetime
from customization import *

import urllib.request,json
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chromeBrowser = webdriver.Chrome("C:\P.S\chromedriver_win32\chromedriver.exe", options=chrome_options)


def steam_scraper(username):
    print("Collecting username information from Steam...")
    steamUrl="https://steamcommunity.com/search/users/#text="+username
    chromeBrowser.get(steamUrl)
    try:
        WebDriverWait(chromeBrowser,5).until(lambda d: d.find_element_by_class_name("searchPersonaName"))
        steamdatas=chromeBrowser.find_elements_by_class_name("searchPersonaName")
        print("---------------------------------------------------------------------------------------\n|Username     |       Profile Link                                                    |\n---------------------------------------------------------------------------------------")

        for steamdata in steamdatas:
            print("---------------------------------------------------------------------------------------")
            print(steamdata.text + " ----------------- " + steamdata.get_property("href"))
            print("---------------------------------------------------------------------------------------")
    except:
        print("This username does not exist or suspended in Steam.")


def reddit_scraper(username):
    print("Collecting username information from Reddit...\n--------------------------------------------------------")

    try:
        reddit = praw.Reddit(client_id=r_client_id, client_secret=r_client_secret, user_agent=r_user_agent)
        redditor=reddit.redditor(username)
        comment_karma=redditor.comment_karma
        link_karma=redditor.link_karma
        total_karma=link_karma+comment_karma
        ts=int(redditor.created_utc)
        created_time=datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
        email_verified=redditor.has_verified_email
        have_subreddit=redditor.subreddit['default_set']
        is_premium=redditor.is_gold
        print("|Username| "+username+" |")
        print("|Karma| " +str(total_karma)+" |")
        print("|Date Created| " +created_time+" |")
        print("|Is Email Verified?| " +str(email_verified)+" |")
        print("|Is Account Premium?| " +str(is_premium)+" |")
        print("|Have any subreddit?| " +str(have_subreddit)+" |")
        if have_subreddit is True:
            print("|Subreddit Name| " +redditor.subreddit["title"]+" |")
        print("--------------------------------------------------------")
    except:
        print("This username does not exist or suspended in Reddit.\n--------------------------------------------------------")


def instagram_scraper(username):
    print("Collecting username information from Instagram\n--------------------------------------------------------")
    insta_url="https://instagram.com/"+username+"/"
    chromeBrowser.get(insta_url)
    WebDriverWait(chromeBrowser,5).until(lambda d: d.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input'))
    try:
        chromeBrowser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(i_email)
        chromeBrowser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(i_password)
        chromeBrowser.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button').click()
        WebDriverWait(chromeBrowser,10).until(lambda d: d.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button'))
        chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        try:
            Name=chromeBrowser.find_element_by_class_name('rhpdm')
        except:
            Name="None"
        try:
            Bio=chromeBrowser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/span')
        except:
            Bio="None"

        Posts=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span')
        try:
            Followers=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
        except:
            Followers=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span')
        try:
            Followings=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span')
        except:
            Followings=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span')
        try:
            PersonalSıte=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/a[1]')
        except NameError:
            PersonalSıte=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/a')
        except:
            PersonalSıte='None'
        def nb_checker(nb):
            try:
                return nb.text
            except:
                return nb

        print("|Real Name | " +nb_checker(Name)+" |")
        print("|Bio|")
        print("| "+nb_checker(Bio)+" |")
        print("|Personal Site| "+nb_checker(PersonalSıte)+" |")
        print("|Followers | " +Followers.text+" |")
        print("|Followings | " +Followings.text+" |")
        print("|Posts | " +Posts.text+" |\n--------------------------------------------------------")
    except:
        print("This username does not exist or suspended in Instagram.\n--------------------------------------------------------")

def github_scraper(username):
    print("Collecting username information from GitHub...\n--------------------------------------------------------")
    githubUrl="https://api.github.com/users/"+username

    try:
        with urllib.request.urlopen(githubUrl) as url:
            githubData=json.loads(url.read().decode())
        print("|Real Name | " +str(githubData['name'])+" |")
        print("|Company | " +str(githubData['company'])+" |")
        print("|Blog | " + str(githubData['blog'])+" |")
        print("|Location | " + str(githubData['location'])+" |")
        print("|E-mail| " + str(githubData['email'])+" |")
        print("|Biography | " + str(githubData['bio'])+" |")
        print("|Twitter Username | " + str(githubData['twitter_username'])+" |")
        print("|Public Repositories | " + str(githubData['public_repos'])+" |")
        print("|Date Created | " + str(githubData['created_at'])+" |")
        print("|Following | " + str(githubData['following'])+" |")
        print("|Followers | " + str(githubData['followers']) + " |\n--------------------------------------------------------")
    except:
        print("This username does not exist or suspended in GitHub.\nOr you exceeded Github's rate limit please try again later.\nPlease consider Authenticating the API.\n--------------------------------------------------------")

def sof_scraper(username):
    chromeBrowser.get('https://stackoverflow.com/users/')
    print("Collecting username information from StackOverFlow...\n--------------------------------------------------------")

    WebDriverWait(chromeBrowser, 10).until(lambda d: d.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div[1]/input'))
    chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div[1]/input').send_keys(username)
    sleep(1)
    try:
        Name=chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/div[2]/a')
        if str(Name.text.lower())==username.lower():
            placeholder=True
        else:
            print("This username does not exist or suspended in StackOverFlow.\n--------------------------------------------------------")
            return None
        try:
            Location=chromeBrowser.find_element_by_class_name('user-location')
            print("|Location | "+Location.text+" |")
        except:
            Location='None'
            print("|Location |" + Location + " |")
        try:
            user_tag = chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/div[3]')
            print("| User Tags/Programming Langs | "+user_tag.text+" |")
        except:
            print("| User Tags/Programming Langs | None |")

        chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/div[2]/a').click()
        WebDriverWait(chromeBrowser, 10).until(lambda d: d.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[2]'))
        try:
            Bio=chromeBrowser.find_element_by_xpath('//*[@id="user-card"]/div/div[2]/div/div[1]/div/div[2]')
            print("|Biography |" + Bio.text + " |")
            input()
        except:
            print("|Biography | None |")
            input()

    except:
        print("This username does not exist or suspended in StackOverFlow1.\n--------------------------------------------------------")
        input()
