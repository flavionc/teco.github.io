const CACHE_NAME = "pwa-cache-v1";
const ASSETS = [
  "./",
  "index.html",
  "TECO.pdf",
  "manifest.webmanifest"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.destination === "image" || req.url.includes("/images/")) {
    event.respondWith(
      fetch(req).catch(() => {
        const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>';
        return new Response(svg, { headers: { "Content-Type": "image/svg+xml" } });
      })
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) {
        return cached;
      }
      return fetch(req).then((response) => {
        const cloned = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(req, cloned);
        });
        return response;
      }).catch(() => caches.match("index.html"));
    })
  );
});