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

})();
