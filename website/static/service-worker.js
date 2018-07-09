self.addEventListener('install', function(event) {
  console.log('Service worker installing...');
  // TODO 3.4: Skip waiting
});

self.addEventListener('activate', function(event) {
  console.log('Service worker activating...');
});