#  Import Statements
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import math
import os

#  Url's for both main campus organizations website
# url = "https://uga.campuslabs.com/engage/organizations/"
url = "https://ua.campuslabs.com/engage/organizations/"

#  base url for each individual uga organization website
# ind_url = "https://uga.campuslabs.com/engage/organization/"
ind_url = "https://ua.campuslabs.com/engage/organization/"
#  Clicks the load more button so that entries can load
def getButton(browser):
    browser.execute_script("document.getElementsByTagName('button')[0].click()")

#  Scrolls the page down so most recent entries can be viewed
def scrollDown(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#  appends all organization data to csv file
def createCSV(driver, url_list):

    global writeFiles
    global writeFile

    arr = ['Number', 'Organization Name', 'Email', 'Phone Number', 'Fax Number'] #  The Labels for each of the columns for the csv file
    index = 1  # index variable used to number each organization when being put in csv file

    #  If file already exists then the file is removed so a new one can be created
    if os.path.exists("./Club_Info.csv"):
        os.remove("./Club_Info.csv")

    # opens premade csv file and appends arr to it
    with open("./Club_Info.csv", 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(arr)

    # closes writer
    writeFile.close()

    for i in url_list:

        #  sleeps for 1 second to prevent loading errors
        time.sleep(1)
        #  goes to specific website url
        driver.get(ind_url + i.rsplit('/', 1)[1])

        #  creates soup of html
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        arr = []

        #  finds all spans with sr-only as class
        info = soup.find_all('span', {'class': 'sr-only'})

        #  find the length of info as that is the number of contact informations the organization provided
        length = len(info)

        #  appends number of org to arr
        arr.append(index)

        #  appends name of org to array
        arr.append(soup.find('h1').text.strip())

        #  checks to see if the org didn't provide any information
        if length != 0:
            #  loops through each piece of contact information
            for k in range(length):
                try:
                    # appends that piece of contact information to array
                    arr.append(info[k].find_parent('div').find_next_sibling('div').text.rsplit(":", 1)[1].strip())
                except:
                    pass

        #  this opens csv file and writes the data in arr to the file
        #  This gives each organization a row with their contact information
        with open("./Club_Info.csv", 'a') as writeFiles:
            writer = csv.writer(writeFiles)
            writer.writerow(arr)

        # increments index for each organization thats added
        index += 1

    #  closes writer after the file has been written to
    writeFiles.close()


#  Main method involved with parsing. Gets all urls from main webpage
def parse():
    try:
        print("Running...")
        inputEntered = 0;
        osDriver = None;
        while inputEntered == 0:
            os = input("Enter Operating System to use (MS Edge, Chrome, Opera, and Firefox): ").lower().replace(" ", "")
            if os == "msedge":
                osDriver = "./msedgedriver"
                inputEntered = 1;
            elif os == "chrome":
                osDriver = "./chromedriver"
                inputEntered = 1;
            elif os == "opera":
                osDriver = "./operadriver"
                inputEntered = 1;
            elif os == "firefox":
                osDriver = "./geckodriver"
                inputEntered = 1;
            else:
                print("Input not accepted. Please enter either: MS Edge, Chrome, Opera, or Firefox")

        #  driver that loads Chrome
        driver = webdriver.Chrome(executable_path=osDriver)

        # used to store all orgnization urls as strings
        child_list = []

        # requests access to uga organizations webpage
        driver.get(url)

        # Waits 2 seconds for website to load to avoid loading issues
        time.sleep(2)

        #  clubs variable is extracted from the webpage and is the total number of webpages that are listed on the website
        clubs = math.ceil((int(driver.find_element_by_xpath("//div[@id='org-search-results']/following-sibling::div").find_element_by_xpath(".//*").text.rsplit(None, 1)[1][:-1]) - 10)/10)
        # adds 5 to clubs
        clubs += 5

        #  This loop clicks the "Load More" button club number of times until all entires have been loaded
        while clubs != 0:

            #  sleeps for 0.5 to avoid loading error
            time.sleep(0.5)
            #  scrolls the window down so user can see most recent entries
            scrollDown(driver)
            try:
                #  clicks button and if all entries are loaded
                #  error for clicking the button is caught and loop is broken out of
                getButton(driver)
            except:
                break

            #  club decrements every time loop goes through
            clubs -= 1

        #  gets all links to club websites and appends them to list
        for child in BeautifulSoup(driver.page_source, "html.parser").find('div', {'id': 'org-search-results'}).find_all('a'):
            child_list.append(child['href'])

        #  creates CSV file
        createCSV(driver, child_list)
        print("Finished!")
    except:
        pass
        print("Error Occurred while running. Program Stopped.")

parse()