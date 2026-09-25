(() => {
  "use strict";

  const API_BASE = "";

  // =========================================================
  // 1. CURSOR SPOTLIGHT TRACKING
  // =========================================================
  window.addEventListener("mousemove", (e) => {
    document.documentElement.style.setProperty("--mouse-x", `${e.clientX}px`);
    document.documentElement.style.setProperty("--mouse-y", `${e.clientY}px`);
  });

  // =========================================================
  // 2. AWWWARDS PARTICLE CANVAS
  // =========================================================
  const canvas = document.getElementById("ambient-canvas");
  const ctx = canvas ? canvas.getContext("2d") : null;
  let particles = [];
  let mouse = { x: null, y: null, radius: 140 };

  function resizeCanvas() {
    if (!canvas) return;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);

  window.addEventListener("mousemove", (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
  });
  window.addEventListener("mouseout", () => {
    mouse.x = null;
    mouse.y = null;
  });

  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.6;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.alpha = Math.random() * 0.4 + 0.15;
    }

    draw() {
      if (!ctx) return;
      ctx.fillStyle = `rgba(139, 92, 246, ${this.alpha})`;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.closePath();
      ctx.fill();
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > canvas.width) this.vx = -this.vx;
      if (this.y < 0 || this.y > canvas.height) this.vy = -this.vy;

      if (mouse.x !== null && mouse.y !== null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouse.radius) {
          const force = (mouse.radius - dist) / mouse.radius;
          this.x -= (dx / dist) * force * 2.5;
          this.y -= (dy / dist) * force * 2.5;
        }
      }
    }
  }

  function initParticles() {
    if (!canvas) return;
    particles = [];
    const count = Math.min(65, Math.floor((canvas.width * canvas.height) / 25000));
    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }
  }
  initParticles();

  function animateCanvas() {
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particles.length; i++) {
      particles[i].draw();
      particles[i].update();

      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 90) {
          ctx.strokeStyle = `rgba(139, 92, 246, ${(1 - dist / 90) * 0.12})`;
          ctx.lineWidth = 0.6;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(animateCanvas);
  }
  if (canvas) animateCanvas();

  // =========================================================
  // 3. COLOR PALETTE SWITCHER
  // =========================================================
  const paletteBtns = document.querySelectorAll(".palette-btn");
  const savedAccent = localStorage.getItem("mhealth_palette") || "cyber";

  function setAccent(color) {
    document.body.dataset.accent = color;
    paletteBtns.forEach((b) => b.classList.toggle("active", b.dataset.color === color));
    localStorage.setItem("mhealth_palette", color);
  }
  setAccent(savedAccent);

  paletteBtns.forEach((b) => {
    b.addEventListener("click", () => setAccent(b.dataset.color));
  });

  // =========================================================
  // 4. QUICK DEMO AUTOFILL
  // =========================================================
  const DEMOS = {
    balanced: {
      age: 21,
      gender: "Male",
      country: "Pakistan",
      academic_level: "Undergraduate",
      most_used_platform: "YouTube",
      purpose_of_use: "Education",
      avg_daily_usage_hours: 3.0,
      daily_unlocks: 40,
      study_hours: 5.0,
      physical_activity_hours: 1.5,
      sleep_hours_per_night: 7.5,
      stress_level: "Low",
    },
    strain: {
      age: 22,
      gender: "Female",
      country: "Pakistan",
      academic_level: "Graduate",
      most_used_platform: "TikTok",
      purpose_of_use: "Entertainment",
      avg_daily_usage_hours: 9.0,
      daily_unlocks: 130,
      study_hours: 1.5,
      physical_activity_hours: 0.2,
      sleep_hours_per_night: 4.5,
      stress_level: "Very High",
    },
  };

  document.querySelectorAll(".demo-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const data = DEMOS[chip.dataset.preset];
      if (!data) return;

      document.getElementById("age").value = data.age;
      document.getElementById("gender").value = data.gender;
      document.getElementById("country").value = data.country;
      document.getElementById("academic_level").value = data.academic_level;
      document.getElementById("most_used_platform").value = data.most_used_platform;
      document.getElementById("purpose_of_use").value = data.purpose_of_use;
      document.getElementById("avg_daily_usage_hours").value = data.avg_daily_usage_hours;
      document.getElementById("daily_unlocks").value = data.daily_unlocks;
      document.getElementById("study_hours").value = data.study_hours;
      document.getElementById("physical_activity_hours").value = data.physical_activity_hours;
      document.getElementById("sleep_hours_per_night").value = data.sleep_hours_per_night;

      segGroup.querySelectorAll(".seg-item").forEach((b) => {
        b.classList.toggle("active", b.dataset.value === data.stress_level);
      });
      stressHiddenInput.value = data.stress_level;

      clearAllErrors();
    });
  });

  // =========================================================
  // 5. GAUGE TICK MARKS
  // =========================================================
  const gaugeTicks = document.getElementById("gauge-ticks");
  function drawTicks() {
    if (!gaugeTicks) return;
    gaugeTicks.innerHTML = "";
    const cx = 130, cy = 145, rOuter = 100, rInner = 88;
    for (let i = 0; i <= 10; i += 2) {
      const angle = Math.PI - (i / 10) * Math.PI;
      const x1 = cx + rOuter * Math.cos(angle);
      const y1 = cy - rOuter * Math.sin(angle);
      const x2 = cx + rInner * Math.cos(angle);
      const y2 = cy - rInner * Math.sin(angle);

      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", x1.toFixed(1));
      line.setAttribute("y1", y1.toFixed(1));
      line.setAttribute("x2", x2.toFixed(1));
      line.setAttribute("y2", y2.toFixed(1));
      gaugeTicks.appendChild(line);
    }
  }
  drawTicks();

  // =========================================================
  // 6. STRESS SEGMENTED BUTTONS
  // =========================================================
  const segGroup = document.getElementById("stress_level_group");
  const stressHiddenInput = document.getElementById("stress_level");
  segGroup.querySelectorAll(".seg-item").forEach((btn) => {
    btn.addEventListener("click", () => {
      segGroup.querySelectorAll(".seg-item").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      stressHiddenInput.value = btn.dataset.value;
      clearFieldError(stressHiddenInput);
    });
  });

  // =========================================================
  // 7. FORM VALIDATION & HELPERS
  // =========================================================
  const form = document.getElementById("predict-form");
  const submitBtn = document.getElementById("submit-btn");
  const resetBtn = document.getElementById("reset-btn");
  const errorRetryBtn = document.getElementById("error-retry-btn");

  const stateIdle = document.getElementById("state-idle");
  const stateLoading = document.getElementById("state-loading");
  const stateResult = document.getElementById("state-result");
  const stateError = document.getElementById("state-error");

  const scoreNumberEl = document.getElementById("score-number");
  const scoreBandEl = document.getElementById("score-band");
  const scoreContextEl = document.getElementById("score-context");
  const gaugeFill = document.getElementById("gauge-fill");
  const signalPill = document.getElementById("signal-pill");

  const hlScreen = document.getElementById("hl-screen");
  const hlSleep = document.getElementById("hl-sleep");
  const hlUnlocks = document.getElementById("hl-unlocks");

  const errorLabelEl = document.getElementById("error-label");
  const errorCopyEl = document.getElementById("error-copy");

  const GAUGE_ARC_LENGTH = 314;

  function fieldWrapper(input) {
    return input ? input.closest(".form-field") : null;
  }

  function setFieldError(input, message) {
    const wrap = fieldWrapper(input);
    if (!wrap) return;
    wrap.classList.add("form-field-invalid");
    const msgEl = wrap.querySelector(".field-error");
    if (msgEl) msgEl.textContent = message;
  }

  function clearFieldError(input) {
    const wrap = fieldWrapper(input);
    if (!wrap) return;
    wrap.classList.remove("form-field-invalid");
    const msgEl = wrap.querySelector(".field-error");
    if (msgEl) msgEl.textContent = "";
  }

  function clearAllErrors() {
    form.querySelectorAll(".form-field").forEach((f) => f.classList.remove("form-field-invalid"));
    form.querySelectorAll(".field-error").forEach((m) => (m.textContent = ""));
  }

  function validate(payload) {
    const errors = [];
    const numericChecks = [
      ["age", 10, 100],
      ["avg_daily_usage_hours", 0, 24],
      ["daily_unlocks", 0, Infinity],
      ["study_hours", 0, 24],
      ["physical_activity_hours", 0, 24],
      ["sleep_hours_per_night", 0, 24],
    ];

    numericChecks.forEach(([key, min, max]) => {
      const input = document.getElementById(key);
      const val = payload[key];
      if (val === "" || val === null || Number.isNaN(val)) {
        errors.push([input, "This field is required."]);
      } else if (val < min || val > max) {
        errors.push([input, `Must be ${min}–${max === Infinity ? "0+" : max}.`]);
      }
    });

    ["gender", "country", "academic_level", "most_used_platform", "purpose_of_use"].forEach((key) => {
      const input = document.getElementById(key);
      if (!payload[key] || String(payload[key]).trim() === "") {
        errors.push([input, "Please select an option."]);
      }
    });

    if (!payload.stress_level) {
      errors.push([stressHiddenInput, "Select a stress level."]);
    }

    return errors;
  }

  function collectPayload() {
    const fd = new FormData(form);
    return {
      age: fd.get("age") === "" ? NaN : parseInt(fd.get("age"), 10),
      gender: fd.get("gender") || "",
      country: (fd.get("country") || "").trim(),
      academic_level: fd.get("academic_level") || "",
      most_used_platform: fd.get("most_used_platform") || "",
      purpose_of_use: fd.get("purpose_of_use") || "",
      avg_daily_usage_hours: fd.get("avg_daily_usage_hours") === "" ? NaN : parseFloat(fd.get("avg_daily_usage_hours")),
      daily_unlocks: fd.get("daily_unlocks") === "" ? NaN : parseInt(fd.get("daily_unlocks"), 10),
      study_hours: fd.get("study_hours") === "" ? NaN : parseFloat(fd.get("study_hours")),
      physical_activity_hours: fd.get("physical_activity_hours") === "" ? NaN : parseFloat(fd.get("physical_activity_hours")),
      sleep_hours_per_night: fd.get("sleep_hours_per_night") === "" ? NaN : parseFloat(fd.get("sleep_hours_per_night")),
      stress_level: fd.get("stress_level") || "",
    };
  }

  function showState(name) {
    [stateIdle, stateLoading, stateResult, stateError].forEach((el) => {
      if (el) el.hidden = true;
    });
    ({ idle: stateIdle, loading: stateLoading, result: stateResult, error: stateError }[name]).hidden = false;
  }

  function setSubmitting(isSubmitting) {
    submitBtn.disabled = isSubmitting;
    submitBtn.classList.toggle("loading", isSubmitting);
  }

  // =========================================================
  // 8. ANIMATED RESULT RENDERING
  // =========================================================
  function animateScoreCounter(targetScore) {
    const duration = 1100;
    const startTime = performance.now();
    const startVal = 0.0;

    function step(now) {
      const elapsed = now - startTime;
      const progress = Math.min(1, elapsed / duration);
      const ease = 1 - Math.pow(1 - progress, 3);
      const val = startVal + (targetScore - startVal) * ease;
      scoreNumberEl.textContent = val.toFixed(2);

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        scoreNumberEl.textContent = targetScore.toFixed(2);
      }
    }
    requestAnimationFrame(step);
  }

  function renderResult(score, p) {
    const clamped = Math.max(0, Math.min(10, score));

    // Dial arc sweep
    gaugeFill.style.transition = "none";
    gaugeFill.style.strokeDashoffset = String(GAUGE_ARC_LENGTH);
    requestAnimationFrame(() => {
      gaugeFill.style.transition = "stroke-dashoffset 1.3s cubic-bezier(0.16, 1, 0.3, 1)";
      const offset = GAUGE_ARC_LENGTH * (1 - clamped / 10);
      gaugeFill.style.strokeDashoffset = String(offset);
    });

    // Pill badge & narrative
    signalPill.className = "signal-pill";
    if (clamped >= 7.0) {
      signalPill.classList.add("pill-optimal");
      scoreBandEl.textContent = "Optimal Balance";
      scoreContextEl.textContent = `Your lifestyle pattern in ${p.country} exhibits superior psychological equilibrium. Controlled social media exposure paired with ${p.sleep_hours_per_night}h of restorative sleep preserves high cognitive endurance.`;
    } else if (clamped >= 5.0) {
      signalPill.classList.add("pill-balanced");
      scoreBandEl.textContent = "Moderate Strain";
      scoreContextEl.textContent = `Your rhythm indicates a manageable student baseline, but screen exposure (${p.avg_daily_usage_hours}h) or phone checks (${p.daily_unlocks}) are exerting noticeable cognitive drag.`;
    } else {
      signalPill.classList.add("pill-strain");
      scoreBandEl.textContent = "Elevated Risk";
      scoreContextEl.textContent = `Elevated strain detected in ${p.country}. Heavy digital consumption (${p.avg_daily_usage_hours}h daily on ${p.most_used_platform}) coupled with ${p.stress_level.toLowerCase()} stress signals immediate fatigue.`;
    }

    // Telemetry updates
    if (hlScreen) hlScreen.textContent = `${p.avg_daily_usage_hours}h`;
    if (hlSleep) hlSleep.textContent = `${p.sleep_hours_per_night}h`;
    if (hlUnlocks) hlUnlocks.textContent = `${p.daily_unlocks}`;

    animateScoreCounter(score);
    showState("result");
  }

  function renderError(label, copy) {
    if (errorLabelEl) errorLabelEl.textContent = label;
    if (errorCopyEl) errorCopyEl.textContent = copy;
    showState("error");
  }

  // =========================================================
  // 9. SUBMIT EVENT LISTENER
  // =========================================================
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearAllErrors();

    const payload = collectPayload();
    const clientErrors = validate(payload);

    if (clientErrors.length > 0) {
      clientErrors.forEach(([input, msg]) => input && setFieldError(input, msg));
      clientErrors[0][0]?.focus?.();
      return;
    }

    setSubmitting(true);
    showState("loading");

    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        let detailMsg = `The API responded with status ${res.status}.`;
        const body = await res.json().catch(() => null);
        if (body && typeof body.detail === "string") detailMsg = body.detail;
        renderError("Prediction Request Failed", detailMsg);
        return;
      }

      const data = await res.json();
      if (typeof data.predicted_mental_health_score !== "number") {
        renderError("Malformed Server Response", "Valid numerical score missing from backend.");
        return;
      }

      renderResult(data.predicted_mental_health_score, payload);
    } catch (err) {
      renderError(
        "Connection Error",
        "Could not communicate with the backend. Ensure FastAPI server is running on port 8000."
      );
    } finally {
      setSubmitting(false);
    }
  });

  // Live input error clearing
  form.querySelectorAll("input, select").forEach((el) => {
    el.addEventListener("input", () => clearFieldError(el));
    el.addEventListener("change", () => clearFieldError(el));
  });

  if (resetBtn) resetBtn.addEventListener("click", () => showState("idle"));
  if (errorRetryBtn) errorRetryBtn.addEventListener("click", () => showState("idle"));
})();
