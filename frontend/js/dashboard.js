const STATUS_LABEL = { pending: 'На рассмотрении', accepted: 'Принята', rejected: 'Отклонена' };
const STATUS_CLASS = { pending: 'status-pending', accepted: 'status-accepted', rejected: 'status-rejected' };

async function initDashboard() {
  const user = requireAuth('login.html');
  if (!user) return;

  setupNavbar();

  document.getElementById('user-greeting').textContent =
    `Привет, ${user.email.split('@')[0]}! 👋`;
  document.getElementById('user-role').textContent =
    user.role === 'student' ? 'Студент' : 'Работодатель';

  if (user.role === 'student') {
    await loadStudentDash();
  } else {
    document.getElementById('employer-section').style.display = 'block';
    await loadEmployerDash();
  }

  // Notifications
  try {
    const notifs = await notifsAPI.list();
    const container = document.getElementById('notif-list');
    if (!notifs.length) {
      container.innerHTML = '<p style="color:var(--muted);font-size:.9rem">Нет новых уведомлений</p>';
    } else {
      container.innerHTML = notifs.map(n => `
        <div style="padding:.6rem 0;border-bottom:1px solid var(--border);font-size:.9rem">${n.text}</div>
      `).join('');
    }
  } catch {}
}

async function loadStudentDash() {
  document.getElementById('student-section').style.display = 'block';
  const tbody = document.getElementById('apps-tbody');
  const stats = { total: 0, pending: 0, accepted: 0, rejected: 0 };

  try {
    const apps = await appsAPI.my();
    stats.total = apps.length;
    apps.forEach(a => stats[a.status]++);

    document.getElementById('stat-total').textContent    = stats.total;
    document.getElementById('stat-pending').textContent  = stats.pending;
    document.getElementById('stat-accepted').textContent = stats.accepted;

    if (!apps.length) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:2rem">Вы ещё не подавали заявок. <a href="index.html" style="color:var(--amber)">Найти вакансии →</a></td></tr>`;
      return;
    }

    tbody.innerHTML = apps.map(a => `
      <tr>
        <td><strong>Вакансия #${a.job_id}</strong></td>
        <td>${new Date(a.created_at).toLocaleDateString('ru')}</td>
        <td>${a.cover ? a.cover.slice(0, 60) + '…' : '—'}</td>
        <td><span class="status-pill ${STATUS_CLASS[a.status]}">${STATUS_LABEL[a.status]}</span></td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:var(--muted)">${err.message}</td></tr>`;
  }
}

async function loadEmployerDash() {
  // Форма создания вакансии
  try {
    const cats = await catsAPI.list();
    const sel = document.getElementById('job-category');
    if (sel) {
      cats.forEach(c => sel.innerHTML += `<option value="${c.id}">${c.name}</option>`);
    }
  } catch {}

  document.getElementById('create-job-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Создаю...';
    try {
      await jobsAPI.create({
        title:       form.title.value,
        description: form.description.value,
        salary:      parseFloat(form.salary.value) || null,
        job_type:    form.job_type.value,
        category_id: parseInt(form.category.value) || null,
        deadline:    form.deadline.value || null,
      });
      toast('Вакансия создана!', 'success');
      form.reset();
      await loadMyJobs();
    } catch (err) {
      toast(err.message, 'error');
    } finally {
      btn.disabled = false; btn.textContent = 'Опубликовать вакансию';
    }
  });

  await loadMyJobs();
}

async function loadMyJobs() {
  const tbody = document.getElementById('jobs-tbody');
  if (!tbody) return;
  tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;padding:1.5rem"><div class="uw-spinner" style="margin:0 auto"></div></td></tr>`;
  try {
    const jobs = await jobsAPI.list();
    const user = getCurrentUser();
    // Filter by current employer
    if (!jobs.length) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align:center;color:var(--muted);padding:2rem">Нет опубликованных вакансий</td></tr>`;
      return;
    }
    tbody.innerHTML = jobs.map(j => `
      <tr>
        <td><strong>${j.title}</strong></td>
        <td>${j.salary ? Math.round(j.salary).toLocaleString('ru') + ' ₸' : '—'}</td>
        <td><span class="status-pill ${j.status === 'open' ? 'status-accepted' : 'status-rejected'}">${j.status === 'open' ? 'Открыта' : 'Закрыта'}</span></td>
        <td>${j.status === 'open' ? `<button onclick="closeJob(${j.id})" class="btn-outline-uw" style="padding:.3rem .9rem;font-size:.82rem">Закрыть</button>` : '—'}</td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:var(--muted)">${err.message}</td></tr>`;
  }
}

async function closeJob(id) {
  try {
    await jobsAPI.close(id);
    toast('Вакансия закрыта', 'success');
    await loadMyJobs();
  } catch (err) {
    toast(err.message, 'error');
  }
}
