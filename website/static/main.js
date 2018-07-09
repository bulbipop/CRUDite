if (!('serviceWorker' in navigator)) {
  console.log('Service worker not supported');
}
navigator.serviceWorker.register('/static/service-worker.js')
.then(function() {
  console.log('Registered');
})
.catch(function(error) {
  console.log('Registration failed:', error);
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$( document ).ready(function() {
	
});
