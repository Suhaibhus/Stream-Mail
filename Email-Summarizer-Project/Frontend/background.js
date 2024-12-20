//This is to make sure that this extension can run on any site. 
chrome.tabs.onUpdated.addListener((tabId, tab) => {
    if (tab.url && tab.url.includes("mail.google.com/mail")) {
        chrome.tabs.sendMessage(tabId, {
            type: "Email_page",
        });
    }
});