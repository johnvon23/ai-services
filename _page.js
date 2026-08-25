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
    var field = canvas.parentElement;
    var main = document.getElementById('main');
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var t = 0;
    var pointerY = 0.5;
    var accentFrac = 0.65;
    var running = false;
    var frame = null;

    function pageTop(el) { return el.getBoundingClientRect().top + window.pageYOffset; }
    function pageBottom(el) { return el.getBoundingClientRect().bottom + window.pageYOffset; }

    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = field.clientWidth * dpr;
      canvas.height = field.clientHeight * dpr;
    }

    /* End the field just above the logo strip, and run the accent line through
       the open space the hero leaves below its copy, never behind the text. */
    function layout() {
      var label = document.querySelector('.strip-label');
      var copy = document.querySelector('.hero-copy');
      var workflow = document.querySelector('.workflow');
      if (label && copy && main) {
        var top = pageTop(main);
        var labelTop = pageTop(label);
        var height = Math.max(320, Math.round(labelTop - top - 12));
        field.style.height = height + 'px';

        var contentBottom = pageBottom(copy);
        if (workflow) contentBottom = Math.max(contentBottom, pageBottom(workflow));
        var target = contentBottom + (labelTop - contentBottom) * 0.5;
        accentFrac = Math.min(0.96, Math.max(0.12, (target - top) / height));
      }
      size();
    }

    function draw() {
      var w = canvas.width;
      var h = canvas.height;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      ctx.clearRect(0, 0, w, h);
      var lines = 20;

      function trace(yBase, amp, phase) {
        ctx.beginPath();
        for (var x = 0; x <= w; x += 7 * dpr) {
          var n = x / w;
          var y = yBase
            + Math.sin(n * 9 + t * 0.9 + phase * 0.7) * amp * 0.55
            + Math.sin(n * 23 - t * 1.4 + phase * 1.3) * amp * 0.3
            + Math.sin(n * 4 + t * 0.5 + phase * 0.2) * amp * 0.4;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // the field swells around the accent line and falls away behind the
      // copy, so the open space carries the graphic and the text stays clean
      function envelope(frac) {
        return Math.exp(-Math.pow((frac - accentFrac) / 0.26, 2));
      }

      for (var i = 0; i < lines; i++) {
        var frac = 0.12 + 0.82 * (i / lines);
        var band = envelope(frac);
        ctx.strokeStyle = 'rgba(152,160,176,' + (0.018 + 0.075 * band) + ')';
        ctx.lineWidth = dpr;
        trace(h * frac, (4 + 26 * band) * dpr * (0.7 + 0.6 * pointerY), i);
      }

      ctx.strokeStyle = 'rgba(255,90,72,0.45)';
      ctx.lineWidth = 1.4 * dpr;
      trace(
        h * accentFrac,
        30 * dpr * (0.7 + 0.6 * pointerY),
        accentFrac * lines
      );

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

    layout();
    if (reduced) {
      t = 4;
      draw();
    } else {
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          if (entries[0].isIntersecting) start();
          else stop();
        }).observe(field);
      } else {
        start();
      }
      window.addEventListener('pointermove', function (e) {
        pointerY = Math.min(1, Math.max(0, e.clientY / window.innerHeight));
      }, { passive: true });
    }

    // text metrics shift once the webfonts land, so re-measure then
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () {
        layout();
        if (!running) draw();
      });
    }

    window.addEventListener('resize', function () {
      layout();
      if (!running) draw();
    });
  }

  setupBooking();
  setupHeader();
  setupBookingComplete();
  setupSignalField();
})();
