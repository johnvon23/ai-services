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

  function setupSignalField() {
    var canvas = document.getElementById('signal-canvas');
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext('2d');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var t = 0;
    var pointerY = 0.5;
    var running = false;
    var frame = null;

    function size() {
      var host = canvas.parentElement;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = host.clientWidth * dpr;
      canvas.height = host.clientHeight * dpr;
    }

    function draw() {
      var w = canvas.width;
      var h = canvas.height;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      ctx.clearRect(0, 0, w, h);
      var lines = 20;
      for (var i = 0; i < lines; i++) {
        var band = Math.pow(Math.sin((i / lines) * Math.PI), 2);
        var yBase = h * 0.12 + (h * 0.82) * (i / lines);
        var amp = (5 + 26 * band) * dpr * (0.7 + 0.6 * pointerY);
        var isAccent = i === 13;
        ctx.beginPath();
        for (var x = 0; x <= w; x += 7 * dpr) {
          var n = x / w;
          var y = yBase
            + Math.sin(n * 9 + t * 0.9 + i * 0.7) * amp * 0.55
            + Math.sin(n * 23 - t * 1.4 + i * 1.3) * amp * 0.3
            + Math.sin(n * 4 + t * 0.5 + i * 0.2) * amp * 0.4;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = isAccent
          ? 'rgba(255,90,72,0.4)'
          : 'rgba(152,160,176,' + (0.035 + 0.06 * band) + ')';
        ctx.lineWidth = (isAccent ? 1.4 : 1) * dpr;
        ctx.stroke();
      }
      t += 0.011;
    }

    function loop() {
      draw();
      if (running) frame = requestAnimationFrame(loop);
    }

    function start() {
      if (running || reduced) return;
      running = true;
      frame = requestAnimationFrame(loop);
    }

    function stop() {
      running = false;
      if (frame) cancelAnimationFrame(frame);
    }

    size();
    if (reduced) {
      t = 4;
      draw();
    } else {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          if (entries[0].isIntersecting) start();
          else stop();
        }).observe(canvas.parentElement);
      } else {
        start();
      }
      window.addEventListener('pointermove', function (e) {
        pointerY = Math.min(1, Math.max(0, e.clientY / window.innerHeight));
      }, { passive: true });
    }
    window.addEventListener('resize', function () {
      size();
      if (!running) draw();
    });
  }

  setupBooking();
  setupHeader();
  setupBookingComplete();
  setupSignalField();
})();
