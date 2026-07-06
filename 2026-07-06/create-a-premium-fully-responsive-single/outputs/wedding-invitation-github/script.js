const invitation = {
  groomName: "Jay",
  brideName: "Janani",
  familyName: "The KVS Family",
  rsvpUrl: "https://forms.gle/example",
  rsvpEmbedUrl: "",
  phone: "+919876543210",
  email: "kvsfamily@example.com",
  reception: {
    title: "J & J Wedding Reception",
    dateLabel: "Sunday, 23 August 2026",
    timeLabel: "6:30 PM onwards",
    start: "2026-08-23T18:30:00+05:30",
    end: "2026-08-23T22:00:00+05:30",
    venue: "Sri Venkateswara Mahal",
    address: "Temple Road, Chennai, Tamil Nadu"
  },
  wedding: {
    title: "J & J Wedding Muhurtham",
    dateLabel: "Monday, 24 August 2026",
    timeLabel: "6:30 AM to 7:30 AM",
    start: "2026-08-24T06:30:00+05:30",
    end: "2026-08-24T07:30:00+05:30",
    venue: "Sri Venkateswara Mahal",
    address: "Temple Road, Chennai, Tamil Nadu"
  },
  travel: {
    mapQuery: "Sri Venkateswara Mahal Chennai",
    railway: "Chennai Central Railway Station",
    airport: "Chennai International Airport",
    busStop: "Temple Road Bus Stop"
  }
};

const qs = (selector, scope = document) => scope.querySelector(selector);
const qsa = (selector, scope = document) => [...scope.querySelectorAll(selector)];

function setText(selector, value) {
  const node = qs(selector);
  if (node) node.textContent = value;
}

function formatICSDate(value) {
  return new Date(value).toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
}

function downloadCalendar(type) {
  const event = invitation[type];
  const location = `${event.venue}, ${event.address}`;
  const body = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//KVS Family//Wedding Invitation//EN",
    "BEGIN:VEVENT",
    `UID:${type}-${Date.now()}@kvs-wedding`,
    `DTSTAMP:${formatICSDate(new Date())}`,
    `DTSTART:${formatICSDate(event.start)}`,
    `DTEND:${formatICSDate(event.end)}`,
    `SUMMARY:${event.title}`,
    `LOCATION:${location}`,
    "DESCRIPTION:With love and gratitude, The KVS Family invites you to bless J & J.",
    "END:VEVENT",
    "END:VCALENDAR"
  ].join("\r\n");

  const blob = new Blob([body], { type: "text/calendar;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${type}-j-and-j.ics`;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function hydrateContent() {
  setText("[data-groom-name]", invitation.groomName);
  setText("[data-bride-name]", invitation.brideName);
  setText("[data-reception-date]", invitation.reception.dateLabel);
  setText("[data-reception-time]", invitation.reception.timeLabel);
  setText("[data-reception-venue]", invitation.reception.venue);
  setText("[data-reception-address]", invitation.reception.address);
  setText("[data-wedding-date]", invitation.wedding.dateLabel);
  setText("[data-wedding-time]", invitation.wedding.timeLabel);
  setText("[data-wedding-venue]", invitation.wedding.venue);
  setText("[data-wedding-address]", invitation.wedding.address);
  setText("[data-railway]", invitation.travel.railway);
  setText("[data-airport]", invitation.travel.airport);
  setText("[data-bus-stop]", invitation.travel.busStop);

  const query = encodeURIComponent(invitation.travel.mapQuery);
  const mapFrame = qs("[data-map-frame]");
  const navigationLink = qs("[data-navigation-link]");
  if (mapFrame) mapFrame.src = `https://www.google.com/maps?q=${query}&output=embed`;
  if (navigationLink) navigationLink.href = `https://www.google.com/maps/search/?api=1&query=${query}`;

  const rsvpLink = qs("[data-rsvp-link]");
  const whatsappLink = qs("[data-whatsapp-link]");
  const phoneLink = qs("[data-phone-link]");
  const emailLink = qs("[data-email-link]");
  const rsvpFrame = qs("[data-rsvp-frame]");

  if (rsvpLink) rsvpLink.href = invitation.rsvpUrl;
  if (whatsappLink) whatsappLink.href = `https://wa.me/${invitation.phone.replace(/\D/g, "")}`;
  if (phoneLink) {
    phoneLink.href = `tel:${invitation.phone}`;
    phoneLink.textContent = invitation.phone.replace(/(\+91)(\d{5})(\d{5})/, "$1 $2 $3");
  }
  if (emailLink) {
    emailLink.href = `mailto:${invitation.email}`;
    emailLink.textContent = invitation.email;
  }
  if (rsvpFrame && invitation.rsvpEmbedUrl) rsvpFrame.src = invitation.rsvpEmbedUrl;
}

function createAmbientElements() {
  const petalField = qs(".petal-field");
  const sparkleField = qs(".sparkle-field");
  const colors = ["#ffb347", "#fff2d1", "#f7d7e5", "#f6a33e", "#fff8e9"];

  for (let i = 0; i < 34; i += 1) {
    const petal = document.createElement("span");
    petal.className = "petal";
    petal.style.left = `${Math.random() * 100}%`;
    petal.style.setProperty("--size", `${0.55 + Math.random() * 0.85}rem`);
    petal.style.setProperty("--duration", `${10 + Math.random() * 12}s`);
    petal.style.setProperty("--delay", `${Math.random() * -16}s`);
    petal.style.setProperty("--drift", `${-45 + Math.random() * 90}vw`);
    petal.style.setProperty("--color", colors[Math.floor(Math.random() * colors.length)]);
    petalField.append(petal);
  }

  for (let i = 0; i < 46; i += 1) {
    const sparkle = document.createElement("span");
    sparkle.className = "sparkle";
    sparkle.style.left = `${Math.random() * 100}%`;
    sparkle.style.setProperty("--duration", `${8 + Math.random() * 10}s`);
    sparkle.style.setProperty("--delay", `${Math.random() * -12}s`);
    sparkle.style.setProperty("--drift", `${-24 + Math.random() * 48}vw`);
    sparkleField.append(sparkle);
  }
}

function setupReveal() {
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add("visible");
      });
    },
    { threshold: 0.18 }
  );
  qsa(".reveal").forEach(element => observer.observe(element));
}

function setupCountdown() {
  const target = new Date(invitation.wedding.start).getTime();
  const parts = {
    days: qs("[data-countdown-days]"),
    hours: qs("[data-countdown-hours]"),
    minutes: qs("[data-countdown-minutes]"),
    seconds: qs("[data-countdown-seconds]")
  };

  const tick = () => {
    const remaining = Math.max(0, target - Date.now());
    const days = Math.floor(remaining / 86400000);
    const hours = Math.floor((remaining % 86400000) / 3600000);
    const minutes = Math.floor((remaining % 3600000) / 60000);
    const seconds = Math.floor((remaining % 60000) / 1000);
    parts.days.textContent = String(days).padStart(2, "0");
    parts.hours.textContent = String(hours).padStart(2, "0");
    parts.minutes.textContent = String(minutes).padStart(2, "0");
    parts.seconds.textContent = String(seconds).padStart(2, "0");
  };

  tick();
  window.setInterval(tick, 1000);
}

function setupNavigation() {
  const toggle = qs(".nav-toggle");
  const links = qsa(".site-nav a");
  const topButton = qs(".back-to-top");

  toggle?.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(isOpen));
  });

  links.forEach(link => {
    link.addEventListener("click", () => {
      document.body.classList.remove("nav-open");
      toggle?.setAttribute("aria-expanded", "false");
    });
  });

  window.addEventListener("scroll", () => {
    topButton?.classList.toggle("visible", window.scrollY > 700);
  }, { passive: true });

  topButton?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
}

function setupInvitationOpening() {
  const openButton = qs("[data-open-invitation]");
  openButton?.addEventListener("click", () => {
    document.body.classList.add("invitation-open");
    qs("#welcome")?.scrollIntoView({ behavior: "smooth" });
  });
  window.setTimeout(() => document.body.classList.add("invitation-open"), 1500);
}

let audioContext;
let ambienceTimer;

function bellTone() {
  if (!audioContext) return;
  const now = audioContext.currentTime;
  [523.25, 659.25, 783.99].forEach((frequency, index) => {
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(frequency, now);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.08 / (index + 1), now + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.4);
    oscillator.connect(gain).connect(audioContext.destination);
    oscillator.start(now);
    oscillator.stop(now + 2.6);
  });
}

function setupAudio() {
  const button = qs("[data-audio-toggle]");
  button?.addEventListener("click", async () => {
    audioContext ||= new AudioContext();
    if (audioContext.state === "suspended") await audioContext.resume();
    if (ambienceTimer) {
      window.clearInterval(ambienceTimer);
      ambienceTimer = undefined;
      button.setAttribute("aria-label", "Play temple ambience");
      return;
    }
    bellTone();
    ambienceTimer = window.setInterval(bellTone, 6500);
    button.setAttribute("aria-label", "Pause temple ambience");
  });
}

function setupCalendarButtons() {
  qsa("[data-calendar]").forEach(button => {
    button.addEventListener("click", () => downloadCalendar(button.dataset.calendar));
  });
}

function setupParallax() {
  const hero = qs(".hero");
  window.addEventListener("scroll", () => {
    const offset = Math.min(80, window.scrollY * 0.08);
    if (hero) hero.style.backgroundPosition = `center calc(50% + ${offset}px)`;
  }, { passive: true });
}

window.addEventListener("load", () => {
  document.body.classList.add("loaded");
});

hydrateContent();
createAmbientElements();
setupReveal();
setupCountdown();
setupNavigation();
setupInvitationOpening();
setupAudio();
setupCalendarButtons();
setupParallax();
