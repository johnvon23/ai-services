window.SITE_CONFIG = {
  bookingUrl: "https://cal.com/john-von-seggern-czdmwr/30min",
  contactEmail: "",
  // Analytics: the project API key ("phc_...") of the PostHog project made for
  // this site. Leave it empty and no analytics script loads.
  posthogKey: "",
  posthogHost: "https://us.i.posthog.com",
  // true counts visitors without cookies, using PostHog's daily anonymous
  // hash. Turn on "Cookieless tracking" in the project's settings first, or
  // PostHog drops the events. false sets no cookies either, but every page
  // load counts as a new visitor.
  posthogCookieless: false
};
