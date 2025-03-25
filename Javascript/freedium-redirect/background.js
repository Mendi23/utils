// Listen for the keyboard shortcut
browser.commands.onCommand.addListener((command) => {
    if (command === "toggle-freedium") {
        // Get the active tab
        browser.tabs.query({ active: true, currentWindow: true })
            .then((tabs) => {
                if (tabs[0]) {
                    const currentUrl = tabs[0].url;

                    // Only process http/https URLs
                    if (currentUrl.startsWith('http')) {
                        // Create the new URL with the freedium.cfd prefix
                        const newUrl = `https://freedium.cfd/${currentUrl}`;

                        // Update the current tab with the new URL
                        browser.tabs.update(tabs[0].id, { url: newUrl });
                    }
                }
            });
    }
}); 