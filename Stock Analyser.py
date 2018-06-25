import sys
import matplotlib
import matplotlib.pyplot
import csv
import ystockquote
from twython import Twython

#############################################################################
TWITTER_APP_KEY = 'ez1MN74tNbL3tpnxOzXFNOpS3'
TWITTER_APP_KEY_SECRET = 'Y4nASXkyDugx2FKWYK4v7KaMfMimuhcH5EWzWRAeirr2bmbnx6'
TWITTER_ACCESS_TOKEN = '1394683742-pw1hq3mp84UzcRaeh7co8Kv0JcQR5w3way0hkmV'
TWITTER_ACCESS_TOKEN_SECRET = 'YWNT4hitS8C5LcywkmofvjlxQGeAjBc5whMjK1KmTXdbJ'
#############################################################################

def scraping_twitter(TWITTER_APP_KEY,TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET ):
    inp = str(input("Please enter a stock quote starting with a $ sign: "))

    file = open("tweets.txt", "w")

    twitter = Twython(app_key=TWITTER_APP_KEY, app_secret=TWITTER_APP_KEY_SECRET, oauth_token=TWITTER_ACCESS_TOKEN, oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

    search = twitter.search(q = inp, count=100)

    tweets=search['statuses']     

    tweet_list = []

    for tweet in tweets:

        print (tweet['text'].encode('utf-8'),'\n')
        tweet_list.append(tweet['text'].encode('utf-8'))



"""
Created by Team U (2015) for CE101 at University of Essex
A prototype Stock Analyser using Twitter API.
"""
def importData(TWITTER_APP_KEY,TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET):

    inp = str(input("Please enter a stock quote starting with a $ sign: "))

    twitter = Twython(app_key=TWITTER_APP_KEY, app_secret=TWITTER_APP_KEY_SECRET, oauth_token=TWITTER_ACCESS_TOKEN, oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

    search = twitter.search(q = inp, count=100)

    tweets=search['statuses']     

    tweet_list = []

    for tweet in tweets:

        #print (tweet['text'].encode('utf-8'),'\n')
        tweet_list.append(tweet['text'].encode('utf-8'))    

    CompanyName = inp
            
    if tweet_list != None:
        readLine = tweet_list
        posTweets = 0
        negTweets = 0
        """
        Words used for Sentiment analysis sourced from https://github.com/jeffreybreen/twitter-sentiment-analysis-tutorial-201107/blob/master/data/opinion-lexicon-English/positive-words.txt
        Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
            Proceedings of the ACM SIGKDD International Conference on Knowledge 
            Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
            Washington, USA, 
        Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
            and Comparing Opinions on the Web." Proceedings of the 14th 
            International World Wide Web conference (WWW-2005), May 10-14, 
            2005, Chiba, Japan.
        """
        wordlistOpened = False
        while wordlistOpened == False:
            try:
                openWordlist = open("positive-words.txt")
                wordlistOpened = True
            except:
                openWordlist = None
                print("Positive word list could not be opened. Please check that it exists.")
                sys.exit(0)
                
        if openWordlist != None:
            readLineWord = openWordlist.readline()
            posWords = []
            while len(readLineWord) > 0:
                if readLineWord[0] != ";":
                    readLineWord = readLineWord.rstrip()
                    #readLineWord = readLineWord.upper()
                    #print(readLineWord)
                    posWords.append((readLineWord).encode('utf-8'))
                readLineWord = openWordlist.readline()
            openWordlist.close()

        wordlistOpened = False
        while wordlistOpened == False:
            try:
                openWordlist = open("negative-words.txt")
                wordlistOpened = True
            except:
                openWordlist = None
                print("Negative word list could not be opened. Please check that it exists.")
                sys.exit(0)
                            
        if openWordlist != None:
            readLineWord = openWordlist.readline()
            negWords = []
            while len(readLineWord) > 0:
                if readLineWord[0] != ";":
                    readLineWord = readLineWord.rstrip()
                    #readLineWord = readLineWord.upper()
                    #print(readLineWord)
                    negWords.append((readLineWord).encode('utf-8'))
                readLineWord = openWordlist.readline()
            openWordlist.close()
  
        posTweets = 1
        negTweets = 1
        for j in range(len(readLine)):
            for i in range(len(posWords)):
                if posWords[i] in readLine[j]:
                    posTweets += 1
                    #print(":)", posTweets)
            for i in range(len(negWords)):
                if negWords[i] in readLine[j]:
                    negTweets += 1
                    #print(":(", negTweets)
           

        noOfTweets = posTweets + negTweets
        
        
        stockinfo = stock_price(CompanyName)
        print("Data successfully imported!")
        return(True, posTweets, negTweets, noOfTweets, "", CompanyName, stockinfo)

def plotPie(storedData):
    CompanyData = (storedData[0][1], storedData[0][2])
    DataLabels = (round((100*storedData[0][1])/(storedData[0][1]+storedData[0][2]),1),round((100*storedData[0][2])/(storedData[0][1]+storedData[0][2]),1))
    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.subplot(211)
    matplotlib.pyplot.pie(CompanyData, explode=None, labels=(DataLabels), colors=("w", "r"), autopct=None, pctdistance =0.6, labeldistance=1.1, shadow=True, startangle=None, radius=None)
    matplotlib.pyplot.show()
    
def exportAllData(storedData):
    try:
        jExportFile = input("Please enter a filename without any file extension: ")
        jExportFile = jExportFile +".csv"
        with open(jExportFile, "w", newline="") as f:
            writer = csv.writer(f, dialect = "excel")
                #writer.writeheader()
            writer.writerow(storedData)
            #writer.writerows(storedData[0][6])
    except:
        print("An error occured during exporting, please try again")
        
def stock_price(CompanyName):
    stockrunning = True
    while stockrunning == True:
        try:
            inp = CompanyName[1:]
            startdate = str(input("Please input a start date for the price check in the form YYYY-MM-DD: "))
            enddate = str(input("Please input an end date for the price check in the form YYYY-MM-DD: "))
            a=ystockquote.get_historical_prices(inp, startdate, enddate)   # prints out stock price between dates.
            return(a)
            stockrunning=False
        except:
            print("An exception has occured please try again.")

    
def exportMenu():
    DataLoaded = False
    exportMenuRunning = True
    storedData = []
    currentData = []
    while exportMenuRunning == True:
        
        print("Welcome to Stock Analyser")
        print("Type 1 to Start and Import Data")
        print("Type 2 to Show Data as Pie Chart")
        print("Type 3 to Load another set of Data")
        print("Type 4 to Export all loaded Data to Excel")
        print("Type 5 to Clear current Data")
        print("Type 6 to Clear all loaded Data")
        print("Type 7 To close")
        menuInput = 0
        while menuInput == 0:
            #try:
            menuInput = int(input("Please select the number for the option: "))
            if menuInput == 1:
                currentData = importData(TWITTER_APP_KEY,TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
                storedData.append(currentData)
            if menuInput == 2:
                plotPie(storedData)
            if menuInput == 3:
                currentData = importData(TWITTER_APP_KEY,TWITTER_APP_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
                storedData.append(currentData)                        
                print("Data Successfully saved")
            if menuInput == 4:
                exportAllData(storedData)
            if menuInput == 5:
                currentData = ()
                storedData = storedData[0:-1]
                print("Current Data cleared")
            if menuInput == 6:
                storedData = []
                print("All loaded Data cleared")
            if menuInput == 7:
                exportMenuRunning = False
            if menuInput <= 0 or menuInput >7:
                print("This is an invalid menu option.")                    
            #except:
                #print("This is an invalid menu option.")
DataLoaded = False
exportMenu()

            

