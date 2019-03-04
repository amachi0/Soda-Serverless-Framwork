def emptystrToNoneInDict(item):
    for k, v in item.items():
        if(type(v) is str):
            if(v == ""):
                item[k] = None

def NoneToEmptystrInDict(item):
    for k, v in item.items():
        if(v is None):
            item[k] = ""