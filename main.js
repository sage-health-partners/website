/* ════════════════════════════════════════════════════════════════════
   SAGE HEALTH — Website behavior
   ════════════════════════════════════════════════════════════════════ */

(function(){
  'use strict';

  const isMobile = () => window.matchMedia('(max-width: 880px)').matches;

  // ───── Sticky header — adds .scrolled when user has moved past the threshold ─────
  const header = document.querySelector('.site-header');
  if (header){
    const setScrolled = () => header.classList.toggle('scrolled', window.scrollY > 16);
    setScrolled();
    window.addEventListener('scroll', setScrolled, {passive:true});
  }

  // ───── Mobile menu drawer ─────
  const menuBtn = document.querySelector('.menu-btn');
  const nav = document.querySelector('.site-nav');
  const backdrop = document.querySelector('.menu-backdrop');
  if (menuBtn && nav){
    const closeMenu = () => {
      nav.classList.remove('open');
      menuBtn.classList.remove('open');
      backdrop && backdrop.classList.remove('open');
      menuBtn.setAttribute('aria-expanded','false');
      document.body.style.overflow='';
      document.querySelectorAll('.nav-dropdown.open').forEach(d => d.classList.remove('open'));
    };
    const openMenu = () => {
      nav.classList.add('open');
      menuBtn.classList.add('open');
      backdrop && backdrop.classList.add('open');
      menuBtn.setAttribute('aria-expanded','true');
      document.body.style.overflow='hidden';
    };
    menuBtn.addEventListener('click', () => {
      nav.classList.contains('open') ? closeMenu() : openMenu();
    });
    backdrop && backdrop.addEventListener('click', closeMenu);
    // Only true navigation links close the drawer — dropdown triggers don't.
    nav.querySelectorAll('a[href]').forEach(a => {
      a.addEventListener('click', () => { if (isMobile()) closeMenu(); });
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  }

  // ───── Mega-menu dropdown — desktop hover + click-toggle, mobile inline expand ─────
  const dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(dd => {
    const trigger = dd.querySelector('.nav-dropdown-trigger');
    if (!trigger) return;
    trigger.setAttribute('aria-haspopup','true');
    trigger.setAttribute('aria-expanded','false');

    trigger.addEventListener('click', e => {
      e.preventDefault();
      e.stopPropagation();
      const wasOpen = dd.classList.contains('open');
      dropdowns.forEach(other => {
        if (other !== dd){
          other.classList.remove('open');
          const t = other.querySelector('.nav-dropdown-trigger');
          t && t.setAttribute('aria-expanded','false');
        }
      });
      dd.classList.toggle('open', !wasOpen);
      trigger.setAttribute('aria-expanded', String(!wasOpen));
    });

    trigger.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' '){
        e.preventDefault();
        trigger.click();
      }
    });
  });

  // Click outside closes any open dropdown (desktop)
  document.addEventListener('click', e => {
    if (isMobile()) return;
    dropdowns.forEach(dd => {
      if (!dd.contains(e.target)){
        dd.classList.remove('open');
        const t = dd.querySelector('.nav-dropdown-trigger');
        t && t.setAttribute('aria-expanded','false');
      }
    });
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape'){
      dropdowns.forEach(dd => {
        dd.classList.remove('open');
        const t = dd.querySelector('.nav-dropdown-trigger');
        t && t.setAttribute('aria-expanded','false');
      });
    }
  });

  // ───── Scroll-reveal animations via IntersectionObserver ─────
  if ('IntersectionObserver' in window){
    const reveal = (entries, observer) => {
      entries.forEach(e => {
        if (e.isIntersecting){
          e.target.classList.add('is-visible');
          observer.unobserve(e.target);
        }
      });
    };
    const obs = new IntersectionObserver(reveal, {
      threshold: 0.12,
      rootMargin: '0px 0px -10% 0px'
    });
    document.querySelectorAll('.reveal,.reveal-stagger').forEach(el => obs.observe(el));
  } else {
    document.querySelectorAll('.reveal,.reveal-stagger').forEach(el => el.classList.add('is-visible'));
  }

  // ───── Year stamp in footer ─────
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  // ───── Hero: typewriter cycling through taglines ─────
  const tw = document.getElementById('hero-typewriter');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (tw && !reducedMotion){
    const taglines = [
      'never missing a call.',
      'with a front desk that never sleeps.',
      'doing more with the same staff.',
      'where nothing falls through the cracks.',
      'finally free from phone tag.',
      'operating at its full potential.'
    ];
    const TYPE_MS = 80;
    const HOLD_MS = 3000;

    tw.textContent = '';
    let lineIdx = 0;

    const sleep = ms => new Promise(r => setTimeout(r, ms));

    const typeLine = async (line) => {
      for (let i = 0; i < line.length; i++){
        tw.textContent = line.slice(0, i + 1);
        await sleep(TYPE_MS);
      }
    };

    (async () => {
      while (true){
        await typeLine(taglines[lineIdx]);
        await sleep(HOLD_MS);
        tw.textContent = '';
        lineIdx = (lineIdx + 1) % taglines.length;
      }
    })();
  }

  // ───── Hero: subtle particle network background ─────
  const canvas = document.getElementById('hero-particles');
  if (canvas && canvas.getContext){
    const hero = canvas.closest('.hero');
    const ctx = canvas.getContext('2d');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    // Brand palette: dark green #2d5a27, teal #0D9488
    const COLORS = [
      'rgba(45,90,39,',     // brand green
      'rgba(13,148,136,'    // brand teal
    ];

    let particles = [];
    let width = 0, height = 0;
    let mouseX = -9999, mouseY = -9999;
    let rafId = null;
    let running = false;

    const targetCount = () => {
      const w = width;
      if (w < 480) return 26;
      if (w < 880) return 42;
      if (w < 1280) return 70;
      return Math.min(110, Math.floor(w / 14));
    };
    const linkDistance = () => width < 880 ? 90 : 130;

    const makeParticle = () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.25,
      r: 1.1 + Math.random() * 1.4,
      color: COLORS[Math.floor(Math.random() * COLORS.length)]
    });

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      width = rect.width;
      height = rect.height;
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = targetCount();
      if (particles.length === 0){
        particles = Array.from({length: count}, makeParticle);
      } else if (particles.length < count){
        while (particles.length < count) particles.push(makeParticle());
      } else if (particles.length > count){
        particles.length = count;
      }
    };

    const step = () => {
      ctx.clearRect(0, 0, width, height);
      const linkD = linkDistance();
      const linkD2 = linkD * linkD;
      const repelD = 110;
      const repelD2 = repelD * repelD;

      for (let i = 0; i < particles.length; i++){
        const p = particles[i];

        // Gentle repel from mouse (falls off smoothly)
        const dx = p.x - mouseX;
        const dy = p.y - mouseY;
        const d2 = dx*dx + dy*dy;
        if (d2 < repelD2 && d2 > 0.001){
          const d = Math.sqrt(d2);
          const force = (1 - d / repelD) * 0.6;
          p.vx += (dx / d) * force * 0.05;
          p.vy += (dy / d) * force * 0.05;
        }

        // Velocity damping so the field stays calm
        p.vx *= 0.985;
        p.vy *= 0.985;
        // Maintain a baseline drift so particles never freeze
        const speed2 = p.vx*p.vx + p.vy*p.vy;
        if (speed2 < 0.005){
          p.vx += (Math.random() - 0.5) * 0.06;
          p.vy += (Math.random() - 0.5) * 0.06;
        }

        p.x += p.vx;
        p.y += p.vy;

        // Wrap edges
        if (p.x < -10) p.x = width + 10;
        else if (p.x > width + 10) p.x = -10;
        if (p.y < -10) p.y = height + 10;
        else if (p.y > height + 10) p.y = -10;

        // Draw the dot
        ctx.beginPath();
        ctx.fillStyle = p.color + '0.55)';
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      }

      // Draw connecting lines
      for (let i = 0; i < particles.length; i++){
        const a = particles[i];
        for (let j = i + 1; j < particles.length; j++){
          const b = particles[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const d2 = dx*dx + dy*dy;
          if (d2 < linkD2){
            const alpha = (1 - Math.sqrt(d2) / linkD) * 0.22;
            ctx.strokeStyle = a.color + alpha + ')';
            ctx.lineWidth = 0.6;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      if (running) rafId = requestAnimationFrame(step);
    };

    const start = () => {
      if (running) return;
      running = true;
      rafId = requestAnimationFrame(step);
    };
    const stop = () => {
      running = false;
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    };

    if (reducedMotion){
      resize();
      step(); // render a single static frame, no RAF loop
    } else {
      resize();
      start();
      window.addEventListener('resize', resize);
      if (hero){
        hero.addEventListener('mousemove', e => {
          const rect = canvas.getBoundingClientRect();
          mouseX = e.clientX - rect.left;
          mouseY = e.clientY - rect.top;
        });
        hero.addEventListener('mouseleave', () => { mouseX = -9999; mouseY = -9999; });
      }
      // Pause when hero scrolls offscreen
      if ('IntersectionObserver' in window && hero){
        const io = new IntersectionObserver(entries => {
          entries.forEach(e => e.isIntersecting ? start() : stop());
        }, {threshold: 0});
        io.observe(hero);
      }
      // Pause when tab is hidden
      document.addEventListener('visibilitychange', () => {
        document.hidden ? stop() : start();
      });
    }
  }

})();
