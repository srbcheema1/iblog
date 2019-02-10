from iblog.const import home_post_len
def prefix(string,l=home_post_len):
    if len(string) < l:
        return string
    else:
        return string[0:l] + " ... "
