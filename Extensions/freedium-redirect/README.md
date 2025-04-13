# Freedium Redirect Firefox Extension

This Firefox extension allows you to quickly open any webpage through the Freedium.cfd service by pressing Cmd+Shift+M (on Mac) or Ctrl+Shift+M (on Windows/Linux).

## Install Signed Version

[One click add](https://addons.mozilla.org/firefox/downloads/file/4461945/d191a8b9c3584345abed-1.0.xpi)
[Developer page](https://addons.mozilla.org/en-US/developers/addon/d191a8b9c3584345abed/)

## What it does

When you press Cmd+Shift+M on a webpage, the extension will redirect the current page to Freedium.cfd, which can be used to bypass paywalls on some websites.

For example:

- If you're on `https://example.com/article`
- Pressing Cmd+Shift+M will redirect you to `https://freedium.cfd/https://example.com/article`

## Installation

### Temporary Installation (for testing)

1. Open Firefox and go to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Navigate to the extension's directory and select the `manifest.json` file

### Permanent Installation

To install the extension permanently:

1. Zip the contents of the extension directory: `cd freedium-redirect && zip -r ../freedium-redirect.zip *`
2. Submit the extension to the [Firefox Add-ons marketplace](https://addons.mozilla.org/developers/)
   - Or sign it yourself if you have a Mozilla developer account

## Usage

Simply press Cmd+Shift+M (on Mac) or Ctrl+Shift+M (on Windows/Linux) when you're on a webpage you want to view through Freedium.

## Customizing the Shortcut

You can change the keyboard shortcut in Firefox:

1. Go to `about:addons`
2. Click the gear icon and select "Manage Extension Shortcuts"
3. Find "Freedium Redirect" and set your preferred shortcut
