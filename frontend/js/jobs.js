const TYPE_LABELS = {
  internship: 'Стажировка',
  part_time:  'Подработка',
  assistant:  'Ассистент',
};
const TYPE_BADGE = {
  internship: 'uw-badge-intern',
  part_time:  'uw-badge-part',
  assistant:  'uw-badge-assistant',
};

function jobCard(job) {
  const initials = job.employer_id ? String(job.employer_id) : '?';
  const salary = job.salary ? `${Math.round(job.salary).toLocaleString('ru')} ₸` : '';
  const deadline = job.deadline ? `до ${new Date(job.deadline).toLocaleDateString('ru')}` : '';
  return `
    <a class="uw-job-card" href="job-detail.html?id=${job.id}">
      <div class="uw-job-card-header">
        <div class="uw-employer-logo">${initials}</div>
        <span class="uw-badge ${TYPE_BADGE[job.job_type] || ''}">${TYPE_LABELS[job.job_type] || job.job_type}</span>
      </div>
      <h3>${job.title}</h3>
      <div class="org">Работодатель #${job.employer_id}</div>
      <div class="uw-job-meta">
        ${deadline ? `<span>📅 ${deadline}</span>` : ''}
      </div>
      ${salary ? `<div class="salary">${salary}</div>` : ''}
    </a>
  `;
}

async function initJobs() {
  setupNavbar();

  const grid     = document.getElementById('jobs-grid');
  const countEl  = document.getElementById('jobs-count');
  const searchIn = document.getElementById('search-input');
  const typeIn   = document.getElementById('search-type');

  // Load categories into filter sidebar
  try {
    const cats = await catsAPI.list();
    const catList = document.getElementById('cat-list');
    if (catList) {
      catList.innerHTML = `<div class="uw-filter-item"><input type="radio" name="cat" id="cat-all" value="" checked><label for="cat-all">Все категории</label></div>`;
      cats.forEach(c => {
        catList.innerHTML += `<div class="uw-filter-item"><input type="radio" name="cat" id="cat-${c.id}" value="${c.id}"><label for="cat-${c.id}">${c.name}</label></div>`;
      });
      catList.querySelectorAll('input').forEach(inp => inp.addEventListener('change', loadJobs));
    }
  } catch {}

  async function loadJobs() {
    grid.innerHTML = `<div class="uw-loader" style="grid-column:1/-1"><div class="uw-spinner"></div>Загрузка...</div>`;
    const catEl = document.querySelector('input[name="cat"]:checked');
    try {
      const jobs = await jobsAPI.list({
        search:      searchIn?.value || '',
        job_type:    typeIn?.value   || '',
        category_id: catEl?.value    || '',
      });
      countEl && (countEl.textContent = jobs.length);
      if (!jobs.length) {
        grid.innerHTML = `<div class="uw-empty" style="grid-column:1/-1"><div class="icon">🔍</div><p>Вакансии не найдены. Попробуйте изменить фильтры.</p></div>`;
        return;
      }
      grid.innerHTML = jobs.map(jobCard).join('');
    } catch (err) {
      grid.innerHTML = `<div class="uw-empty" style="grid-column:1/-1"><div class="icon">⚠️</div><p>${err.message}</p></div>`;
    }
  }

  // Events
  document.getElementById('search-btn')?.addEventListener('click', loadJobs);
  searchIn?.addEventListener('keydown', e => e.key === 'Enter' && loadJobs());
  typeIn?.addEventListener('change', loadJobs);

  loadJobs();
}
