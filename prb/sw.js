const CACHE='prb-research-v1.5.0-rights-1';
const FILES=['./','./index.html','./app.js','./styles.css','./manifest.webmanifest','./icon-192.png','./icon.svg','./rights.html'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('prb-research-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  const url=new URL(e.request.url);
  if(e.request.method!=='GET'||url.origin!==self.location.origin||!url.pathname.startsWith(new URL(self.registration.scope).pathname))return;
  const shell=url.pathname.endsWith('/app.js')||url.pathname.endsWith('/styles.css')||url.pathname.endsWith('/index.html')||url.pathname===new URL(self.registration.scope).pathname;
  if(shell){e.respondWith(fetch(e.request).then(response=>{if(response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(e.request,copy)).catch(()=>{});}return response;}).catch(()=>caches.match(e.request)));return;}
  e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request)));
});