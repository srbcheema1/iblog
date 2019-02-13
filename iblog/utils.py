from iblog.const import home_post_len
from bs4 import BeautifulSoup
def prefix(string,l=home_post_len):
    string = BeautifulSoup(string,'html.parser').text
    if len(string) < l:
        return string
    else:
        return string[0:l] + " ... "
