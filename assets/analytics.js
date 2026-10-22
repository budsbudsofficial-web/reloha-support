/* RELOHA website analytics: one initialization per top-level document. */
(function () {
  'use strict';
  if (window.top !== window.self || window.__relohaAnalytics) return;
  var base = '/reloha-support/';
  if (location.pathname === base || location.pathname === base + 'index.html') {
    var phone = /iPhone|iPod|Android.*Mobile|Windows Phone/i.test(navigator.userAgent || '');
    var narrow = window.matchMedia && window.matchMedia('(max-width:720px)').matches;
    var query = new URLSearchParams(location.search);
    if ((phone && query.get('desktop') !== '1') || (narrow && !query.has('desktop'))) return;
  }
  window.__relohaAnalytics = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', 'G-073EKNSKE9', {
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });
  var tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtag/js?id=G-073EKNSKE9';
  document.head.appendChild(tag);
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var url;
    try { url = new URL(link.href, location.href); } catch (_) { return; }
    if (url.hostname !== 'apps.apple.com' || !/\/id6813563330(?:[/?]|$)/.test(url.pathname)) return;
    window.gtag('event', 'app_store_click', {
      link_url: url.origin + url.pathname,
      page_path: location.pathname,
      link_placement: link.closest('.feature') ? 'article_feature' : 'site_cta',
      transport_type: 'beacon'
    });
  });
})();
