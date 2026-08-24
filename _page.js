(function () {
  'use strict';

  function track(name, payload) {
    try {
      window.dataLayer = window.dataLayer || [];
      var event = { event: name };
      if (payload) {
        for (var key in payload) {
          if (Object.prototype.hasOwnProperty.call(payload, key)) event[key] = payload[key];
        }
      }
      window.dataLayer.push(event);
    } catch (err) {}
  }

  function bookingUrl() {
    return window.SITE_CONFIG && window.SITE_CONFIG.bookingUrl;
  }

  function setupBooking() {
    var url = bookingUrl();
    var links = document.querySelectorAll('[data-book]');
    for (var i = 0; i < links.length; i++) {
      (function (el) {
        if (url) el.setAttribute('href', url);
        el.addEventListener('click', function (e) {
          track('book_session_click', { placement: el.getAttribute('data-book') });
          if (!url) {
            e.preventDefault();
            var message = document.getElementById('booking-soon');
            if (message) {
              message.hidden = false;
              message.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
          }
        });
      })(links[i]);
    }
  }

  function setupHeader() {
    var header = document.querySelector('header.site');
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function setupBookingComplete() {
    window.addEventListener('message', function (e) {
      var data = e.data;
      if (!data) return;
      var scheduled = data.event === 'calendly.event_scheduled' ||
        (typeof data === 'string' && data.indexOf('calendly.event_scheduled') !== -1);
      if (scheduled) track('booking_completed');
    });
  }

  setupBooking();
  setupHeader();
  setupBookingComplete();
})();
