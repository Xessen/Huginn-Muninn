from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from prettytable import PrettyTable
from time import sleep
from customization import *

import urllib.request,json
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chromeBrowser = webdriver.Chrome("C:\P.S\chromedriver_win32\chromedriver.exe", options=chrome_options)
def bio_shortener(bio):
    lines=[]
    x=len(bio)/30
    y=0
    Status=True
    while Status:
        y=y+1
        lines.append(bio[0:30])
        lines.append("\n")
        bio=bio[30:]
        if y==int(x)+1:
            Status=False

    A=''.join(lines)
    return A

def nb_checker(nb):
    if nb!='None':
        return nb.text
    else:
        nb


def quick_search(username):
    print("Collecting username information...")
    insta_url="https://instagram.com/"+username+"/"
    chromeBrowser.get(insta_url)
    WebDriverWait(chromeBrowser,5).until(lambda d: d.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input'))
    chromeBrowser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(i_email)
    chromeBrowser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(i_password)
    chromeBrowser.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button').click()
    WebDriverWait(chromeBrowser,10).until(lambda d: d.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button'))
    chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    try:
        instaName=chromeBrowser.find_element_by_class_name('rhpdm').text
    except:
        instaName="None"
    try:
        instaBio=chromeBrowser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/span').text
    except:
        instaBio="None"
    try:
        instaPersonalSite=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/a[1]').text
    except NameError:
        instaPersonalSite=chromeBrowser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/a').text
    except:
        instaPersonalSite='None'

    sleep(1)
    chromeBrowser.get('https://stackoverflow.com/users/')
    WebDriverWait(chromeBrowser, 10).until(lambda d: d.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div[1]/input'))
    chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[1]/div[1]/input').send_keys(username)
    sleep(1)
    try:
        Name=chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/div[2]/a')
        if str(Name.text.lower())==username.lower():
            placeholder=True
    except:
        return None
    try:
        sofLocation=chromeBrowser.find_element_by_class_name('user-location').text
    except:
        sofLocation='None'
    try:
        sofUser_tag = chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/div[3]').text
    except:
        sofUser_tag='None'

    chromeBrowser.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/div[2]/a').click()
    WebDriverWait(chromeBrowser, 10).until(lambda d: d.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[2]'))
    try:
        sofBio=chromeBrowser.find_element_by_xpath('//*[@id="user-card"]/div/div[2]/div/div[1]/div/div[2]').text
    except:
        sofBio='None'

    githubUrl = "https://api.github.com/users/" + username

    try:
        with urllib.request.urlopen(githubUrl) as url:
            githubData = json.loads(url.read().decode())
            gitName=str(githubData['name'])
            gitCompany=str(githubData['company'])
            gitBlog=str(githubData['blog'])
            gitEmail=str(githubData['email'])
            gitBio=str(githubData['bio'])
            gitTwitter=str(githubData['twitter_username'])
            gitLocation=str(githubData['location'])
    except:
        placeholder=True

    pt = PrettyTable(
        [' ', '         Instagram         ', '         StackOverflow         ', '         GitHub         '])
    pt.add_row(["Name", instaName,"X", gitName])
    pt.add_row(["Email", "X","X",gitEmail])
    pt.add_row(["Company","X","X", gitCompany])
    pt.add_row(["Personal Site", instaPersonalSite,"X", gitBlog])
    pt.add_row(["Location", "X", sofLocation, gitLocation])
    pt.add_row(["Twitter", "X", "X", gitTwitter])
    pt.add_row(["Tags", "X", sofUser_tag, "X"])
    pt.add_row(["Biography", bio_shortener(instaBio), bio_shortener(sofBio), bio_shortener(gitBio)])
    print(pt)
    input()