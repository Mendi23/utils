Useful resources and tools I've found while trying to create little 'hooks' and 'hacks' to make my life easier while using the browser.

**Important**: this aren't web-development tools per se, but snippets and links around API's for the browser itself. (although, everything is still JS)


I'm using firefox, but since most modern browser are using chromium and the chrome toolkit, the resources should work cross-platform.

## Firefox's `Browser Console`

It's seems that this is not very known, and there are better alternatives (mainly: ___), but it's very useful for some simple stuff, and it's available right out-of-the-box.

see [here](https://developer.mozilla.org/en-US/docs/Tools/Browser_Console) for how to use it (basically: `about:config -> devtools.chrome.enabled = true` and then <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>J</kbd>)
), [here](https://marcosc.com/2015/01/gecko-gbrowser-and-tabs/) and [here](https://developer.mozilla.org/en-US/docs/Archive/Add-ons/Tabbed_browser) for a quick intro.

The tool's main strength is the `gBrowser` namespace directly accessible in the console, and all the commands it enables.

This tool is officially obsolete, but it still works as of Firefox 84. you can find the main reference page [here](https://developer.mozilla.org/en-US/docs/Archive/Mozilla/XUL/XUL_Reference). the important elements to know are [browser](https://developer.mozilla.org/en-US/docs/Archive/Mozilla/XUL/browser) [tabbrowser](https://developer.mozilla.org/en-US/docs/Archive/Mozilla/XUL/tabbrowser) and [tab](https://developer.mozilla.org/en-US/docs/Archive/Mozilla/XUL/tab).

While reviewing the docs, you'll notice all the links are broken. just change every link from `https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XUL/*` to: `https://developer.mozilla.org/en-US/docs/Archive/Mozilla/XUL/*` and you'll get the content you seek.

```javascript
gBrowser.addTab("http://www.google.com/", {triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()})
// or
gBrowser.addTrustedTab("http://www.google.com/");
// and to remove:
gBrowser.removeTab(tab); // Don't use tab.remove(). can cause memory leaks
```

You can see [examples](https://gist.github.com/Gozala/7476658) for more uses. from my limited experience, the `load` tab even doesn't work properly.

## Web Console


## webextensions
[running locally](https://extensionworkshop.com/documentation/develop/getting-started-with-web-ext/)  
[creating extension](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension)  
[the API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API)

## Changing default page styles
[create userChrome.css](https://www.userchrome.org/how-create-userchrome-css.html)  
[Replace firefox default favicon](https://allanhutchison.net/2011/11/15/replace-firefox-default-favicon/)  

## misc.
