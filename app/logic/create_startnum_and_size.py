def createStartNumAndSize(page):
    if page == 0:
        startNum = 0
        size = 3
    else:
        startNum = 3 + (page - 1) * 5
        size = 5

    return startNum, size
