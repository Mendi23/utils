document.addEventListener('DOMContentLoaded', function () {
    const addToButton = document.getElementById('addToButton');
    const statusDiv = document.getElementById('status');
    const loader = document.getElementById('loader');

    addToButton.addEventListener('click', function () {
        // Show loading state
        addToButton.disabled = true;
        loader.style.display = 'inline-block';
        statusDiv.textContent = 'Finding articles...';

        // Send message to content script to collect article links
        browser.tabs.query({ active: true, currentWindow: true })
            .then(tabs => {
                return browser.tabs.sendMessage(tabs[0].id, { action: "getArticleLinks" });
            })
            .then(response => {
                if (response && response.links && response.links.length > 0) {
                    statusDiv.textContent = `Found ${response.links.length} article links. Adding to Pocket...`;

                    // Send links to background script for Pocket API handling
                    return browser.runtime.sendMessage({
                        action: "addToPocket",
                        links: response.links,
                        domain: response.domain
                    });
                } else {
                    throw new Error("No article links found");
                }
            })
            .then(result => {
                loader.style.display = 'none';
                addToButton.disabled = false;
                statusDiv.textContent = `Added ${result.success} article(s) to Pocket. ${result.failed} failed.`;
            })
            .catch(error => {
                loader.style.display = 'none';
                addToButton.disabled = false;
                statusDiv.textContent = `Error: ${error.message}`;
                console.error(error);
            });
    });
}); 