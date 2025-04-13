# Bulk Add to Pocket

A Firefox extension to find all article links on a webpage and add them to Pocket with a domain-based tag.

## Features

- Scans the current page for article links
- Adds all found links to Pocket in bulk
- Automatically tags all links with the domain name
- Simple, easy-to-use interface

## Installation

### Temporary Installation (for development)

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox" in the sidebar
3. Click "Load Temporary Add-on..."
4. Navigate to the extension's directory and select the `manifest.json` file

### Creating a Distributable Package

1. Zip the contents of this directory (make sure to include actual PNG files for the icons)
2. Rename the zip file to have a `.xpi` extension
3. Submit to the Firefox Add-ons store or distribute manually

## Usage

1. Navigate to a webpage containing article links
2. Click on the Bulk Add to Pocket extension icon in the toolbar
3. Click the "Add All Articles to Pocket" button
4. Wait for the extension to scan and add links to your Pocket account
5. All added links will be tagged with the website's domain name

## Important Notes

- Before using this extension, you need to register an application on the Pocket Developer Portal to get a consumer key
- Replace `YOUR_POCKET_CONSUMER_KEY` in `background.js` with your actual Pocket consumer key
- Replace the placeholder icon files with actual PNG images

## Requirements

- Firefox 57 or later
- A Pocket account

## License

MIT
