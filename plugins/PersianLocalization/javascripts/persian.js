/**
 * Persian UI polish: document title and hard-coded "Matomo" strings in the DOM.
 */
(function () {
    if (document.documentElement.lang !== 'fa') {
        return;
    }

    document.documentElement.setAttribute('dir', 'rtl');

    function localizeMatomoLabel(text) {
        if (!text || typeof text !== 'string') {
            return text;
        }
        return text
            .replace(/\bMatomo\b/g, 'ماتومو')
            .replace(/\bPiwik\b/g, 'ماتومو');
    }

    if (document.title) {
        document.title = localizeMatomoLabel(document.title);
    }

    var observer = new MutationObserver(function () {
        if (document.title) {
            var localized = localizeMatomoLabel(document.title);
            if (document.title !== localized) {
                document.title = localized;
            }
        }
    });
    observer.observe(document.querySelector('title') || document.head, {
        subtree: true,
        characterData: true,
        childList: true,
    });
})();
