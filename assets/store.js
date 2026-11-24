// Shows AutoMetronom's App Store button and the cross-link on the Canu pages
// as soon as Apple's public lookup lists the app. Until then nothing changes.
(function () {
    var callback = "amStore" + Date.now();
    window[callback] = function (data) {
        var app = data && data.results && data.results[0];
        if (!app || !app.trackViewUrl) { return; }
        document.querySelectorAll("[data-am-live]").forEach(function (element) { element.hidden = false; });
        document.querySelectorAll("[data-am-store]").forEach(function (element) {
            var link = document.createElement("a");
            link.className = "button";
            link.href = app.trackViewUrl;
            link.textContent = element.getAttribute("data-am-store");
            element.replaceWith(link);
        });
    };
    var script = document.createElement("script");
    script.src = "https://itunes.apple.com/lookup?bundleId=net.allroundnetwork.autometronom&callback=" + callback;
    document.head.appendChild(script);
})();
