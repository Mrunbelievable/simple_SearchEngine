import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk
import json
from urllib.parse import urlparse
import urllib.robotparser


def scraper(url, resp):
    if 200<=int(resp.status)<=226 and resp.raw_response != None: #check response status
        print("scraping")
        try:
            i = open("report.json", "r")
            report = json.load(i)
            i.close()
        except IOError:
            report = {}
            print("generating report")
        soup = BeautifulSoup(resp.raw_response.content, parser = "html.parser")
        update_word_freqeuncy(soup, url, report) #check low information
        update_pages_num(url, report)
        update_subdomain(url, report)
        links = extract_next_links(url, resp, soup, report)
        print("writing to json file")
        with open("report.json", "w") as o:
            json.dump(report, o, indent = 4, sort_keys = True)
        return links 
    else:
        return []

def extract_next_links(url, resp, soup, report):
    domains = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu",
                        "today.uci.edu/department/information_computer_sciences"]
    tag_list = soup.find_all("a")
    url_list = []
    for tag in tag_list:
        if tag.get('href') != None:
            temp = tag.get('href').split("#")[0]
            for domain in domains:
                if domain in temp and temp not in url_list and temp not in report["----------Unique_Pages----------"]: #make sure pages are unique and belongs to listed domain
                    url_list.append(temp)
                    break
    url_list = list(set(url_list))
    if len(url_list) != 0:
        url_list = check_robot_file(url_list) #check robots.txt
    return url_list


def is_valid(url):
    try:
        parsed = urlparse(url)
        #check traps
        if parsed.scheme not in {"http", "https"} or "replytocom=" in url\
            or (parsed.netloc == "wics.ics.uci.edu" and parsed.path.startswith("/event"))\
            or ("calender" in parsed.path and "day" in parsed.path) or "/pdf/" in parsed.path:
            return False
    
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
            + r"|replytocom=)$", parsed.path.lower())
        #else:
            #return False
    except TypeError:
        print("TypeError for ", parsed)
        raise

#update word frequency and longest page and write into json file
def update_word_freqeuncy(soup: BeautifulSoup, url, report):
    #tokenize the content
    tokenizer = nltk.RegexpTokenizer(r"[a-zA-Z.\'\-_]+")  #define a tokenizer
    url_context = ""
    for string in soup.stripped_strings:
        url_context = url_context + string 
    word_list = tokenizer.tokenize(url_context)
    low_information_flag = False
    longest = len(word_list) #logestpage update by looking at len(word_list)
    if longest <= 10: #if word numbers <= 10, it is low information
        low_information_flag = True
    
    #move stop words out
    stop_words_list = ['a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep\tkeeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure\tt', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve", 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero']
    fdic = FreqDist(word_list)  
    for stop_word in stop_words_list:
        if stop_word in fdic.keys():
            del fdic[stop_word]
    
    if len(fdic.keys()) <= 10: #if word in word frequency dict <= 10, it is low information
        low_information_flag = True
    
    #update longest page to json file
    if "----------Longest_Num----------" not in report:
        report["----------Longest_Num----------"] = 0
        report["----------Longest_Url----------"] = []
    if longest > report["----------Longest_Num----------"]:
        report["----------Longest_Num----------"] = longest
        report["----------Longest_Url----------"] = url
            
    if not low_information_flag: # if it has high information value, update word frequency to json file
        for key, value in fdic.items():
            if key in report.keys():
                report[key] += fdic[key]
            else:
                report[key] = fdic[key]

#update subdomain to json file
def update_subdomain(url, report):
    try:
        if "----------ics.uci.edu----------" not in report:
            report["----------ics.uci.edu----------"] = {}
        hostname = urlparse(url).hostname
        if hostname.endswith(".ics.uci.edu"):
            if hostname in report["----------ics.uci.edu----------"]:
                report["----------ics.uci.edu----------"][hostname] += 1
            elif hostname not in report["----------ics.uci.edu----------"]:
                report["----------ics.uci.edu----------"][hostname] = 1
    except TypeError:
        print("TypeError:",parsed)

#update unique page to json file       
def update_pages_num(url, report):
    if "----------Unique_Pages----------" not in report:
        report["----------Unique_Pages----------"] = []
    elif url not in report["----------Unique_Pages----------"]:
        report["----------Unique_Pages----------"].append(url)

#check robots.txt file and validity for each link list
def check_robot_file(url_list):
    rp_ics = urllib.robotparser.RobotFileParser("https://www.ics.uci.edu/robots.txt")
    rp_ics.read()
    rp_cs = urllib.robotparser.RobotFileParser("https://www.cs.uci.edu/robots.txt")
    rp_cs.read()
    rp_in4 = urllib.robotparser.RobotFileParser("https://www.informatics.uci.edu/robots.txt")
    rp_in4.read()
    rp_stat = urllib.robotparser.RobotFileParser("https://www.stat.uci.edu/robots.txt")
    rp_stat.read()
    rp_today = urllib.robotparser.RobotFileParser("https://today.uci.edu/robots.txt")
    rp_today.read()
    url_list2 = (i for i in url_list)
    for url in url_list2:
        parsed = urlparse(url)
        if parsed.netloc.endswith("ics.uci.edu"):
            if not rp_ics.can_fetch("*", url) or not is_valid(url):
                if url in url_list:
                    print("REMOVING:  ", url, "  FROM LIST")
                    url_list.remove(url)
        if parsed.netloc.endswith("cs.uci.edu"):
            if not rp_cs.can_fetch("*", url) or not is_valid(url):
                if url in url_list:
                    print("REMOVING:  ", url, "  FROM LIST")
                    url_list.remove(url)
        if parsed.netloc.endswith("informatics.uci.edu"):
            if not rp_in4.can_fetch("*", url) or not is_valid(url):
                if url in url_list:
                    print("REMOVING:  ", url, "  FROM LIST")
                    url_list.remove(url)
        if parsed.netloc.endswith("stat.uci.edu"):
            if not rp_stat.can_fetch("*", url) or not is_valid(url):
                if url in url_list:
                    print("REMOVING:  ", url, "  FROM LIST")
                    url_list.remove(url)
        if parsed.netloc.endswith("today.uci.edu"):
            if not rp_today.can_fetch("*", url) or not is_valid(url):
                if url in url_list:
                    print("REMOVING:  ", url, "  FROM LIST")
                    url_list.remove(url)

    return url_list