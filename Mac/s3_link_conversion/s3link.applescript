set inputURI to the clipboard
if inputURI starts with "s3://" then
    set cleanedURI to text 6 thru -1 of inputURI
    set AppleScript's text item delimiters to "/"
    set bucketName to text item 1 of cleanedURI
    set keyPath to (text items 2 thru -1 of cleanedURI) as text
    set AppleScript's text item delimiters to ""
    
    set consoleURL to "https://us-east-1.console.aws.amazon.com/s3/buckets/" & bucketName & "?region=us-east-1&bucketType=general&prefix=" & keyPath & "&showversions=false"
    
    set the clipboard to consoleURL
    display notification "AWS Console URL copied!" with title "S3 URI Converted"
else
    display dialog "Not a valid S3 URI!" buttons {"OK"} default button "OK"
end if
