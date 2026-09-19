(() => {
  const menu = document.querySelector('.mobile-nav');
  if (menu) {
    const close = (restoreFocus = false) => {
      if (!menu.open) return;
      menu.open = false;
      if (restoreFocus) menu.querySelector('summary').focus();
    };
    document.addEventListener('keydown', event => { if (event.key === 'Escape') close(true); });
    document.addEventListener('click', event => { if (!menu.contains(event.target)) close(); });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => close()));
    window.matchMedia('(min-width: 801px)').addEventListener('change', event => { if (event.matches) close(); });
  }
  const filters = document.querySelector('[data-publication-filters]');
  if (!filters) return;
  filters.hidden = false;
  const search = document.querySelector('#paper-search');
  const year = document.querySelector('#paper-year');
  const papers = [...document.querySelectorAll('[data-paper]')];
  const groups = [...document.querySelectorAll('[data-year]')];
  const count = document.querySelector('[data-result-count]');
  const empty = document.querySelector('[data-empty]');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const apply = () => {
    const words = normalize(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    papers.forEach(paper => {
      const text = normalize(paper.dataset.search);
      const matches = (!year.value || paper.closest('[data-year]').dataset.year === year.value) && words.every(word => text.includes(word));
      paper.hidden = !matches;
      if (matches) visible++;
    });
    groups.forEach(group => { group.hidden = ![...group.querySelectorAll('[data-paper]')].some(paper => !paper.hidden); });
    count.textContent = `${visible} ${visible === 1 ? 'publication' : 'publications'}${search.value.trim() || year.value ? ' found' : ''}`;
    empty.hidden = visible !== 0;
  };
  search.addEventListener('input', apply);
  year.addEventListener('change', apply);
  filters.addEventListener('submit', event => event.preventDefault());
  filters.addEventListener('reset', () => {
    search.value = '';
    year.value = '';
    apply();
    search.focus();
  });
  apply();
})();
