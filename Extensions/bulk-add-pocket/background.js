// Listen for messages from the popup
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "addToPocket") {
        addLinksToPocket(message.links, message.domain)
            .then(result => {
                sendResponse(result);
            })
            .catch(error => {
                console.error("Error adding to Pocket:", error);
                sendResponse({ success: 0, failed: message.links.length, error: error.message });
            });

        return true; // Indicates async response
    }
});

/**
 * Add multiple links to Pocket with domain tag
 */
async function addLinksToPocket(links, domain) {
    if (!links || links.length === 0) {
        return { success: 0, failed: 0 };
    }

    // Initialize counters
    let successCount = 0;
    let failedCount = 0;

    // Create a tag from the domain name
    const tag = domain.replace(/\./g, '_');

    // We need to check if user is already authenticated with Pocket
    const isAuthenticated = await checkPocketAuth();

    if (!isAuthenticated) {
        // Redirect user to Pocket authentication
        await authenticateWithPocket();
    }

    // Process each link
    for (const url of links) {
        try {
            await addToPocket(url, tag);
            successCount++;
        } catch (error) {
            console.error(`Failed to add ${url} to Pocket:`, error);
            failedCount++;
        }

        // Small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 300));
    }

    return {
        success: successCount,
        failed: failedCount
    };
}

/**
 * Check if user is authenticated with Pocket
 */
async function checkPocketAuth() {
    // Check if we have access token in storage
    try {
        const data = await browser.storage.local.get('pocket_access_token');
        return !!data.pocket_access_token;
    } catch (error) {
        console.error("Error checking Pocket auth:", error);
        return false;
    }
}

/**
 * Authenticate with Pocket using OAuth
 */
async function authenticateWithPocket() {
    // Pocket Consumer Key - this should be obtained from Pocket's developer portal
    // For the purpose of this example, we'll use a placeholder
    const consumerKey = "YOUR_POCKET_CONSUMER_KEY";

    // Step 1: Obtain a request token
    const requestToken = await getRequestToken(consumerKey);

    // Step 2: Redirect user to Pocket authorization page
    await redirectToAuth(requestToken, consumerKey);

    // Step 3: User authorizes the app, and we get the access token
    // This happens after the redirect back to our extension
    return new Promise((resolve, reject) => {
        // This is handled by the redirect_uri callback
        // We'll simulate completion for this demo
        // In a real extension, you'd handle the redirect properly
        resolve(true);
    });
}

/**
 * Get a request token from Pocket
 */
async function getRequestToken(consumerKey) {
    const response = await fetch('https://getpocket.com/v3/oauth/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Accept': 'application/json'
        },
        body: JSON.stringify({
            consumer_key: consumerKey,
            redirect_uri: 'https://getpocket.com/auth/success'
        })
    });

    if (!response.ok) {
        throw new Error(`Failed to get request token: ${response.status}`);
    }

    const data = await response.json();

    // Store the request token
    await browser.storage.local.set({ pocket_request_token: data.code });

    return data.code;
}

/**
 * Redirect user to Pocket auth page
 */
async function redirectToAuth(requestToken, consumerKey) {
    const authUrl = `https://getpocket.com/auth/authorize?request_token=${requestToken}&redirect_uri=https://getpocket.com/auth/success`;

    // Open auth URL in a new tab
    await browser.tabs.create({ url: authUrl });

    // After user authorizes, we should get the access token
    // This would be handled through the redirect URI
    // For simplicity, we'll simulate this process

    // In a real extension, you would implement a proper OAuth flow
    // with a redirect handler that captures the access token

    // Simulating access token for this example
    await browser.storage.local.set({
        pocket_access_token: 'sample_access_token',
        pocket_username: 'user'
    });
}

/**
 * Add a single URL to Pocket with a tag
 */
async function addToPocket(url, tag) {
    // Get access token and consumer key
    const data = await browser.storage.local.get(['pocket_access_token', 'pocket_consumer_key']);
    const accessToken = data.pocket_access_token;

    // For demo purposes - in a real extension, you'd use your app's consumer key
    const consumerKey = "YOUR_POCKET_CONSUMER_KEY";

    // Check if we have the token
    if (!accessToken) {
        throw new Error('Not authenticated with Pocket');
    }

    // Make the add request to Pocket API
    const response = await fetch('https://getpocket.com/v3/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Accept': 'application/json'
        },
        body: JSON.stringify({
            url: url,
            consumer_key: consumerKey,
            access_token: accessToken,
            tags: tag
        })
    });

    if (!response.ok) {
        throw new Error(`Failed to add to Pocket: ${response.status}`);
    }

    return await response.json();
} 