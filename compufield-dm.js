/* Compufield Digital Marketing — small site behaviours (no libraries) */
(function () {
  "use strict";

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Courses dropdown
  var dd = document.querySelector(".nav-courses");
  if (dd) {
    var btn = dd.querySelector("button");
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = dd.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!dd.contains(e.target)) { dd.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { dd.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }
    });
  }

  // Hub hero: the query types itself, then the result appears
  var hero = document.querySelector(".serp-hero");
  if (hero) {
    var box = hero.querySelector(".searchbox");
    var q = hero.querySelector(".q");
    var full = q ? q.getAttribute("data-q") : "";
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!q || reduce) {
      if (q) q.textContent = full;
      if (box) box.classList.add("done");
    } else {
      hero.classList.add("typing");
      q.textContent = "";
      var i = 0;
      var tick = function () {
        i++;
        q.textContent = full.slice(0, i);
        if (i < full.length) { setTimeout(tick, 38 + Math.random() * 40); }
        else { setTimeout(function () { hero.classList.remove("typing"); box.classList.add("done"); }, 260); }
      };
      setTimeout(tick, 350);
    }
  }

  // Lite YouTube: load the player only when clicked
  document.querySelectorAll(".yt[data-id]").forEach(function (el) {
    var id = el.getAttribute("data-id");
    el.style.backgroundImage = "url(https://i.ytimg.com/vi/" + id + "/hqdefault.jpg)";
    el.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
      f.title = el.getAttribute("aria-label") || "Student review video";
      f.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
      f.allowFullscreen = true;
      el.innerHTML = "";
      el.appendChild(f);
    }, { once: true });
  });

  // Demo forms: timing token (spam check in PHP) + error message after a failed send
  var params = new URLSearchParams(window.location.search);
  document.querySelectorAll("form.demo-form").forEach(function (form) {
    var ts = form.querySelector("input[name=ts]");
    if (ts) ts.value = Math.floor(Date.now() / 1000);
    var back = form.querySelector("input[name=page]");
    if (back) back.value = window.location.pathname.split("/").pop() || "digital_marketing_course_mumbai.html";

    var c = params.get("course");
    if (c) {
      var sel = form.querySelector("select[name=course]");
      if (sel) Array.prototype.forEach.call(sel.options, function (o) { if (o.value === c) sel.value = c; });
    }

    if (params.get("demo") === "error" && !form.querySelector(".notice")) {
      var n = document.createElement("p");
      n.className = "notice notice--err";
      n.setAttribute("role", "alert");
      n.textContent = params.get("why") === "fields"
        ? "Please add your name and a 10-digit mobile number, then send again."
        : "Your request didn't go through. Please try again, or WhatsApp us on +91 98201 34058.";
      form.insertBefore(n, form.firstChild);
    }

    form.addEventListener("submit", function (e) {
      var phone = form.querySelector("input[name=phone]");
      var digits = (phone.value || "").replace(/\D/g, "");
      if (digits.length < 10) {
        e.preventDefault();
        phone.setCustomValidity("Enter a 10-digit mobile number");
        phone.reportValidity();
        phone.addEventListener("input", function () { phone.setCustomValidity(""); }, { once: true });
        return;
      }
      var b = form.querySelector("button[type=submit]");
      if (b) { b.disabled = true; b.textContent = "Sending…"; }
    });
  });
})();
