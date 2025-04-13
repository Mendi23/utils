// Listen for messages from the popup
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getArticleLinks") {
        const links = collectArticleLinks();
        const domain = extractDomain(window.location.hostname);

        sendResponse({
            links: links,
            domain: domain
        });
    }
    return true; // Required for async response
});

/**
 * Collects all article links from the current page
 */
function collectArticleLinks() {
    const articleLinks = [];
    const allLinks = document.querySelectorAll('a');

    // Common article link patterns
    const articlePatterns = [
        // Links containing article indicators in URL
        /\/(article|post|blog|news)\//,
        /\/(20\d{2})\/\d{1,2}\/\d{1,2}\//,  // Date pattern like /2023/01/15/

        // Links that might be articles based on their structure
        /\.html$/,
        /\/(p|story)\/[a-zA-Z0-9-]+$/,

        // Common news/blog platforms
        /medium\.com\/.*\/[a-zA-Z0-9-]+-[a-f0-9]+$/,
        /nytimes\.com\/\d{4}\/\d{2}\/\d{2}\//,
        /washingtonpost\.com\/.*\/\d{4}\/\d{2}\/\d{2}\//
    ];

    // Process all links on the page
    allLinks.forEach(link => {
        const href = link.href;

        // Skip if not a valid URL or it's a same-page anchor
        if (!href || href.startsWith('javascript:') || href.startsWith('#')) {
            return;
        }

        // Skip certain file types and non-article URLs
        if (href.match(/\.(jpg|jpeg|png|gif|css|js|pdf|zip|mp3|mp4)$/i)) {
            return;
        }

        // Check if URL matches article patterns or if element has article indicators
        const isArticleUrl = articlePatterns.some(pattern => href.match(pattern));
        const isInArticleSection = isElementInArticleSection(link);
        const hasArticleAttributes = hasArticleRelatedAttributes(link);

        if (isArticleUrl || isInArticleSection || hasArticleAttributes) {
            // Avoid duplicates
            if (!articleLinks.includes(href)) {
                articleLinks.push(href);
            }
        }
    });

    return articleLinks;
}

/**
 * Checks if element is inside an article section
 */
function isElementInArticleSection(element) {
    // Check ancestors for article indicators
    let current = element;

    // Go up 5 levels at most
    for (let i = 0; i < 5 && current; i++) {
        const tagName = current.tagName ? current.tagName.toLowerCase() : '';

        // Check for article semantic tags
        if (['article', 'main', 'section'].includes(tagName)) {
            return true;
        }

        // Check for article-related class or id names
        const classAndId = (current.className || '') + ' ' + (current.id || '');
        if (/(article|post|blog|story|news|content)/i.test(classAndId)) {
            return true;
        }

        current = current.parentElement;
    }

    return false;
}

/**
 * Checks if element has attributes indicating it's an article link
 */
function hasArticleRelatedAttributes(element) {
    // Check aria attributes, rel, classes, etc.
    const attributes = element.attributes;
    for (let i = 0; i < attributes.length; i++) {
        const attrName = attributes[i].name;
        const attrValue = attributes[i].value;

        if (/(article|post|blog|story|news|content)/i.test(attrName + ' ' + attrValue)) {
            return true;
        }
    }

    return false;
}

/**
 * Extract the base domain name from a hostname
 */
function extractDomain(hostname) {
    // Remove 'www.' prefix if present
    let domain = hostname.replace(/^www\./, '');

    // Extract main domain (without subdomain if any)
    const parts = domain.split('.');
    if (parts.length > 2) {
        // Handle common multi-part TLDs like .co.uk, .com.au
        if (parts[parts.length - 2].length <= 3 && parts[parts.length - 1].length <= 3) {
            domain = parts[parts.length - 3] + '.' + parts[parts.length - 2] + '.' + parts[parts.length - 1];
        } else {
            domain = parts[parts.length - 2] + '.' + parts[parts.length - 1];
        }
    }

    return domain;
} 