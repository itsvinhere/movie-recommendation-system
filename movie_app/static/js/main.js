/* ============================================================
   CineVault — Main JavaScript
   ============================================================ */

// ─── Navbar scroll effect ─────────────────────────────────
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNav');
  if (nav) {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  }
});

// ─── Toast helper ─────────────────────────────────────────
function showToast(message, type = 'default') {
  const toastEl = document.getElementById('liveToast');
  const msgEl = document.getElementById('toastMessage');
  if (!toastEl || !msgEl) return;

  msgEl.textContent = message;
  toastEl.className = 'toast align-items-center text-white border-0';
  if (type === 'error') toastEl.style.borderLeft = '3px solid #e50914';
  else if (type === 'success') toastEl.style.borderLeft = '3px solid #22c55e';
  else toastEl.style.borderLeft = '3px solid #666';

  const toast = bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 2800 });
  toast.show();
}

// ─── Create movie card HTML (for dynamic loading) ─────────
function createMovieCard(movie) {
  const poster = movie.poster_url || `https://via.placeholder.com/300x450/1a1a2e/e50914?text=${encodeURIComponent(movie.title)}`;
  const genre = movie.genre ? movie.genre.split('|')[0] : 'Movie';
  const overview = movie.overview ? movie.overview.substring(0, 100) + '...' : '';

  return `
    <div class="movie-card" onclick="window.location.href='/movie/${movie.id}'">
      <div class="movie-poster-wrap">
        <img src="${poster}" alt="${escHtml(movie.title)}" class="movie-poster"
             onerror="this.src='https://via.placeholder.com/300x450/1a1a2e/e50914?text=No+Image'">
        <div class="movie-overlay">
          <div class="movie-overlay-content">
            <a href="/movie/${movie.id}" class="btn-play-sm" onclick="event.stopPropagation()">
              <i class="bi bi-play-fill"></i>
            </a>
            <div class="movie-quick-info">
              <span class="rating-badge"><i class="bi bi-star-fill"></i> ${movie.imdb_rating || 'N/A'}</span>
              <span class="year-badge">${movie.release_year || ''}</span>
            </div>
            <p class="movie-overview-preview">${escHtml(overview)}</p>
          </div>
        </div>
      </div>
      <div class="movie-info">
        <h6 class="movie-title">${escHtml(movie.title)}</h6>
        <div class="movie-genre">${escHtml(genre)}</div>
      </div>
    </div>
  `;
}

function escHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// ─── Mood filter (footer links) ───────────────────────────
function filterMood(mood) {
  window.location.href = `/?mood=${mood}`;
}

// ─── Search bar keyboard shortcut (/  to focus) ───────────
document.addEventListener('keydown', (e) => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
    e.preventDefault();
    const si = document.querySelector('.search-input');
    if (si) si.focus();
  }
  if (e.key === 'Escape') {
    const si = document.querySelector('.search-input');
    if (si) si.blur();
  }
});

// ─── Smooth horizontal scroll with mouse wheel ────────────
document.querySelectorAll('.movies-row').forEach(row => {
  row.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) {
      e.preventDefault();
      row.scrollBy({ left: e.deltaY * 2, behavior: 'smooth' });
    }
  }, { passive: false });
});

// ─── Lazy image loading ───────────────────────────────────
if ('IntersectionObserver' in window) {
  const imgObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          imgObserver.unobserve(img);
        }
      }
    });
  }, { rootMargin: '100px' });

  document.querySelectorAll('img[data-src]').forEach(img => imgObserver.observe(img));
}

// ─── Movie card hover animations using JS for mobile ──────
document.querySelectorAll('.movie-card').forEach(card => {
  card.addEventListener('touchstart', () => card.classList.add('hover-active'));
  card.addEventListener('touchend', () => {
    setTimeout(() => card.classList.remove('hover-active'), 500);
  });
});

// ─── Active nav link highlight ────────────────────────────
document.querySelectorAll('.nav-link-custom').forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});

// ─── Init ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Apply saved mood if present
  const savedMood = localStorage.getItem('selectedMood');
  if (savedMood) {
    localStorage.removeItem('selectedMood');
    const pill = document.querySelector(`[onclick="selectMood('${savedMood}')"]`);
    if (pill) {
      setTimeout(() => {
        pill.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        pill.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 600);
    }
  }

  // Animate cards on load
  const cards = document.querySelectorAll('.movie-card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, Math.min(i * 60, 600));
  });
});
