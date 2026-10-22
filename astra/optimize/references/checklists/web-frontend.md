# Web frontend

Measure on a mid-tier mobile device profile with network throttling, and with field data (RUM, CrUX) when it exists; a fast desktop on office Wi-Fi hides most of the cost.

## Metrics

Transferred bytes (compressed, per route), request count and critical-chain depth, TTFB, FCP, LCP, INP, CLS, total blocking time, JS parse and compile time, long tasks on the main thread, frame time during scrolling and animation, JS heap and DOM node count, energy on battery devices.

## Levers

- **Ship less code**: static generation or server rendering, islands or partial hydration, zero-JS pages where interaction allows, per-route code splitting, tree shaking, replacing heavy dependencies, dropping polyfills for browsers you do not support.
- **Fewer and earlier requests**: inline critical CSS, preload the LCP resource, `fetchpriority`, preconnect, 103 Early Hints, HTTP/2 or HTTP/3, removing request waterfalls (data fetched in parallel or on the server).
- **Smaller bytes**: Brotli 11 or zstd for static assets, AVIF or WebP with `srcset` at displayed size, SVG optimization, font subsetting and WOFF2, purging unused CSS, minification.
- **Caching**: content-hashed assets with `Cache-Control: immutable`, CDN and edge caching, service worker for repeat visits, `stale-while-revalidate`.
- **Main thread**: break long tasks, move compute to Web Workers or WASM, avoid layout thrashing (batch reads before writes), `content-visibility`, list virtualization, fewer re-renders (memoization, signals, stable keys), animations on `transform` and `opacity` only.
- **Memory**: detach listeners and observers, release large objects, cap caches, avoid retaining DOM in closures.

Changes users can see (image quality, font choice, dropped animations, supported browsers) need the user.

## Tools

Lighthouse and Lighthouse CI, WebPageTest, Chrome DevTools Performance, Coverage and Memory panels, `web-vitals`, bundle analyzers (`esbuild --metafile`, `rollup-plugin-visualizer`, `source-map-explorer`), `size-limit`.
