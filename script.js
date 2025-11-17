/* script.js — merged and cleaned
   - Dropdown toggles for nav (click to open)
   - Accordion behavior: submenu -> show corresponding accordion content
   - Image autocomplete search (optional images)
   - Mock text search + results + media detail toggling
   - Exposes window.showMediaDetail for inline onclick usage
*/

(function () {
  /* Simple selectors */
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));

  /* --------------------------
     NAV DROPDOWN TOGGLE
     - Anchors with class .dropbtn toggle their sibling .dropdown
  ----------------------------*/
  function initDropdowns() {
    // Find all anchors that have a sibling .dropdown (treat as dropbtn)
    $$('.nav-menu > li').forEach((li) => {
      const anchor = li.querySelector('a');
      const dropdown = li.querySelector('.dropdown');
      if (anchor && dropdown) {
        anchor.classList.add('dropbtn');
        anchor.addEventListener('click', (e) => {
          e.preventDefault();
          // Toggle this dropdown, close others
          $$('.dropdown').forEach((d) => {
            if (d !== dropdown) d.classList.remove('show');
          });
          dropdown.classList.toggle('show');
        });
      }
    });

    // Close dropdowns if clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-menu')) {
        $$('.dropdown').forEach((d) => d.classList.remove('show'));
      }
    });
  }

  /* --------------------------
     ACCORDION: clicking submenu items with data-target
     shows the corresponding .accordion-content and hides others
  ----------------------------*/
  function initAccordionBehavior() {
    // Attach delegated click handler to nav for links with data-target
    const nav = $('.nav-menu');
    if (!nav) return;

    nav.addEventListener('click', (e) => {
      const link = e.target.closest('a[data-target]');
      if (!link) return;
      e.preventDefault();
      const targetId = link.getAttribute('data-target');
      if (!targetId) return;

      // Hide all accordion-content elements, then show the target
      $$('.accordion-content').forEach((el) => {
        if (el.id === targetId) {
          el.style.display = 'block';
        } else {
          el.style.display = 'none';
        }
      });

      // Close all dropdowns
      $$('.dropdown').forEach((d) => d.classList.remove('show'));

      // Smooth scroll the target section into view (if exists)
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    // On init hide all accordion-content blocks
    $$('.accordion-content').forEach((el) => (el.style.display = 'none'));
  }

  /* --------------------------
     Image-based Autocomplete Search (optional)
     - uses #search-input and #search-results containers
     - Replace mediaImages array with your real assets if you want
  ----------------------------*/
  function initImageSearch() {
    const mediaImages = [
      // update these with real image paths in your project if you want thumbnails
      { name: 'The Martian', src: 'martian.jpg', link: '#detail-book1' },
      { name: 'Dune', src: 'dune.jpg', link: '#detail-film1' },
      { name: 'Time Magazine', src: 'time.jpg', link: '#detail-mag1' },
    ];

    const input = $('#search-input');
    const results = $('#search-results');
    if (!input || !results) return;

    results.style.display = 'none';
    results.innerHTML = '';

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      results.innerHTML = '';
      if (!q) {
        results.style.display = 'none';
        return;
      }

      const filtered = mediaImages.filter((m) => m.name.toLowerCase().includes(q));
      if (filtered.length === 0) {
        results.style.display = 'none';
        return;
      }

      filtered.forEach((m) => {
        const img = document.createElement('img');
        img.src = m.src;
        img.alt = m.name;
        img.title = m.name;
        img.style.cursor = 'pointer';
        img.addEventListener('click', () => {
          // If link is an anchor to your page, navigate there
          if (m.link && m.link.startsWith('#')) {
            const anchorId = m.link.substring(1);
            // show target detail if it exists
            const el = document.getElementById(anchorId);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // also try to toggle the corresponding detail block
            if (anchorId.startsWith('detail-')) {
              $$('.media-detail-block').forEach((b) => b.classList.remove('is-active'));
              const target = document.getElementById(anchorId);
              if (target) target.classList.add('is-active');
            }
          } else if (m.link) {
            window.open(m.link, '_self');
          }
        });
        results.appendChild(img);
      });

      results.style.display = 'flex';
    });

    // hide results if clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-container')) results.style.display = 'none';
    });
  }

  /* --------------------------
     Mock text search and result handling (from your earlier script.js)
     - uses #search-button, #search-input, #results-container
     - shows "View Details" button which opens a detail block
  ----------------------------*/
  function initMockTextSearch() {
    const searchBtn = $('#search-button');
    const searchInput = $('#search-input');
    const resultsContainer = $('#results-container');

    // mock data — replace with API calls when backend ready
    const mockData = [
      { name: 'The Python Primer', author: 'A. Developer', category: 'Book', id: 'detail-book1' },
      { name: 'Project Deployment', author: 'B. Analyst', category: 'Film', id: 'detail-film1' },
      { name: 'Flask Insights Q3', author: 'C. Engineer', category: 'Magazine', id: 'detail-mag1' },
    ];

    if (!searchBtn || !searchInput || !resultsContainer) return;

    searchBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const term = searchInput.value.trim().toLowerCase();

      // Clear previous detail displays
      $$('.media-detail-block').forEach((block) => block.classList.remove('is-active'));

      // Ensure default detail shows if exists
      const defaultDetail = $('#detail-default');
      if (defaultDetail) defaultDetail.classList.add('is-active');

      if (!term) {
        resultsContainer.innerHTML = `<p style="font-style: italic; color: #555;">Please enter a search term.</p>`;
        return;
      }

      const found = mockData.find(
        (item) => item.name.toLowerCase().includes(term) ||
                  (item.author && item.author.toLowerCase().includes(term))
      );

      if (found) {
        resultsContainer.innerHTML = `
          <div class="search-result-item">
            <h4>${escapeHtml(found.name)}</h4>
            <p>By: ${escapeHtml(found.author)} (${escapeHtml(found.category)})</p>
            <button class="search-detail-button" data-target="${escapeHtml(found.id)}">View Details</button>
          </div>
        `;
        const btn = resultsContainer.querySelector('.search-detail-button');
        if (btn) {
          btn.addEventListener('click', function () {
            const tid = this.dataset.target;
            $$('.media-detail-block').forEach(b => b.classList.remove('is-active'));
            const t = document.getElementById(tid);
            if (t) t.classList.add('is-active');
            t && t.scrollIntoView({ behavior: 'smooth', block: 'start' });
          });
        }
      } else {
        resultsContainer.innerHTML = `<p style="font-style: italic; color: #555;">No results found for "${escapeHtml(term)}".</p>`;
      }
    });

    // On load ensure only default detail block is active
    document.addEventListener('DOMContentLoaded', () => {
      $$('.media-detail-block').forEach((block) => {
        if (block.id !== 'detail-default') block.classList.remove('is-active');
        else block.classList.add('is-active');
      });
    });
  }

  /* --------------------------
     showMediaDetail - used by inline onclick attributes
  ----------------------------*/
  function showMediaDetail(clickedElement) {
    if (!clickedElement) return;
    const targetId = clickedElement.getAttribute('data-target');
    if (!targetId) return;
    $$('.media-detail-block').forEach(b => b.classList.remove('is-active'));
    const t = document.getElementById(targetId);
    if (t) t.classList.add('is-active');
    t && t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  // expose globally so inline handlers work
  window.showMediaDetail = showMediaDetail;

  /* --------------------------
     small helper: escape HTML
  ----------------------------*/
  function escapeHtml(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#039;');
  }

  /* --------------------------
     Init all
  ----------------------------*/
  function initAll() {
    try {
      initDropdowns();
      initAccordionBehavior();
      initImageSearch();
      initMockTextSearch();
    } catch (err) {
      console.error('Initialization error:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
