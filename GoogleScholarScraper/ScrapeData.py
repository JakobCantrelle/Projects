import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

############################## FUCNTIONS #################################

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
# Provide the name for the text file
def SimplifyCaseTitle(case_title):
    simplified_title = re.sub(r',\s\d+.*$', '', case_title)
    if len(simplified_title) > 128:
        return simplified_title[:128-3] + '..'
    else:
        return simplified_title

# Remove things like page breaks
def RemoveGarbage(DirtyString):
    cleaned_text = re.sub(r'\s+', ' ', DirtyString)
    return cleaned_text.strip()

#Send text to a text document in Output
def OutputText(text):
    FileName = SimplifyCaseTitle(text[0:300]) + ".txt"
    FileName = FileName.replace("\\", "")
    outputFolderPath = os.path.join(os.getcwd(), 'Output')
    
    if not os.path.exists(outputFolderPath):
        os.makedirs(outputFolderPath)
    
    filePath = os.path.join(outputFolderPath, FileName)
    
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(text)

# Takes a page num and search query and gives you a good URL
def GenerateBaseURL(SearchQuery, Page):
    SearchQuery = SearchQuery.replace(' ', '+')
    StartOn = (Page - 1) * 10
    return ScholarURL + PreStart + str(StartOn) + PreQuery + SearchQuery + PostQuery





# Find links on page and put them into a nice little list
def GetLinksFromPage(ParsedHTML):
    PageLinks = set()
    for link in ParsedHTML.find_all('a', href=True):
        full_url = urljoin(ScholarURL, link['href'])
        if urlparse(full_url).netloc == urlparse(ScholarURL).netloc:
            lowerURL = full_url.lower()
            IsGoodPage = 'scholar_case?case=' in lowerURL
            if IsGoodPage:
                PageLinks.add(full_url)
                
    return PageLinks













############################## MAIN #######################################


# Do not change this
ScholarURL = "https://scholar.google.com"
PreStart = "/scholar?start="
PreQuery = "&q="
PostQuery = "&hl=en&as_sdt=8000006"

# What you're searching for on the website
SearchQuery = "Academy"

# How many pages to parse? 1 page is 10 text documents.
# Too much of this gets me blocked. good thing i have a vpn on my laptop
HowManyPagesToParse = 6

TotalDocuments = 10 * HowManyPagesToParse
CurrentDocument = 1



for i in range(HowManyPagesToParse):
    # Go through the search results and find every webpage
    ParseTestURL = GenerateBaseURL(SearchQuery, i + 1)
    BaseSearchPage = requests.get(ParseTestURL, headers=headers)
    BaseSearchParse = BeautifulSoup(BaseSearchPage.text, 'html.parser')
    print("BASE URL: " + ParseTestURL)
    URLS = GetLinksFromPage(BaseSearchParse)



    MassiveString = ""
    for url in URLS:
        # Go through every link on the search results, get text, and dump it into a file in the 'Output' folder
        Requested = requests.get(url, headers=headers)
        Parsed = BeautifulSoup(Requested.text, 'html.parser')
        for ScriptOrStyle in Parsed(["script", "style"]):
            ScriptOrStyle.decompose()
        TextFragments = [Element.get_text() for Element in Parsed.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        CleanText = ' '.join(TextFragment.strip() for TextFragment in TextFragments)
        CleanText = RemoveGarbage(CleanText)
        print("(" + str(CurrentDocument) + "/" + str(TotalDocuments) + ") " + SimplifyCaseTitle(CleanText[0:300]) + ".txt")
        OutputText(CleanText)
        CurrentDocument += 1
