
def getLine(f: str) -> str:
    """
    Read line from txt file
    :param f file: 
    :return string: 
    """
    line = f.readline(100)
    if len(line) == 0:
        return ''
    while line[0] == '#' or line[0] == '\n':
        line = ''
        line = f.readline(100)
        if len(line) == 0:
            return ''
    return line
