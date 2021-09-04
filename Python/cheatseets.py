
def regex_flags():
    import re
    
    re.split("[,.:]", s) # split multiple 

    re.X # allow comments and multiline patterns 
    pattern = """(?x)
    from [ ]+ [0-9:]+  # start time
    [ ]+
    to [ ]+ [0-9:]+    # end time
    """

    "\s - whitespace"

    re.I # ignorecase

    re.M # `^`` and `$` match the beginnings and ends of lines instead of the whole text.

    re.S # `.` also match newline
