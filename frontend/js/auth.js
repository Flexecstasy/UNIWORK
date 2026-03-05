/* ─── Shared helpers ──────────────────────────────────────────────── */

function toast(msg, type = 'success') {
  let el = document.getElementById('uw-toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'uw-toast';
    el.className = 'uw-toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.className = `uw-toast ${type}`;
  setTimeout(() => el.classList.add('show'), 10);
  setTimeout(() => el.classList.remove('show'), 3500);
}

function getCurrentUser() {
  try { return JSON.parse(localStorage.getItem('uw_user')); } catch { return null; }
}

function requireAuth(redirectTo = 'login.html') {
  if (!getToken()) { window.location.href = redirectTo; return null; }
  return getCurrentUser();
}

function setupNavbar() {
  const user = getCurrentUser();
  const token = getToken();
  const navRight = document.getElementById('nav-right');
  if (!navRight) return;

  if (token && user) {
    navRight.innerHTML = `
      <li><a href="dashboard.html">👤 Кабинет</a></li>
      <li><a href="#" id="logout-btn" class="btn-nav">Выйти</a></li>
    `;
    document.getElementById('logout-btn').addEventListener('click', (e) => {
      e.preventDefault();
      removeToken();
      window.location.href = 'index.html';
    });
  } else {
    navRight.innerHTML = `
      <li><a href="login.html">Войти</a></li>
      <li><a href="register.html" class="btn-nav">Регистрация</a></li>
    `;
  }

  // Hamburger
  const burger = document.getElementById('uw-burger');
  if (burger) {
    burger.addEventListener('click', () => {
      document.getElementById('uw-nav-links').classList.toggle('open');
    });
  }
}

/* ─── Login page ──────────────────────────────────────────────────── */

async function initLogin() {
  if (getToken()) { window.location.href = 'index.html'; return; }

  const form = document.getElementById('login-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Вхожу...';
    try {
      const data = await authAPI.login({
        email:    form.email.value,
        password: form.password.value,
      });
      setToken(data.access_token);
      const user = await authAPI.me();
      localStorage.setItem('uw_user', JSON.stringify(user));
      toast('Добро пожаловать!', 'success');
      setTimeout(() => window.location.href = 'index.html', 700);
    } catch (err) {
      toast(err.message, 'error');
      btn.disabled = false; btn.textContent = 'Войти';
    }
  });
}

/* ─── Register page ───────────────────────────────────────────────── */

async function initRegister() {
  if (getToken()) { window.location.href = 'index.html'; return; }

  const form = document.getElementById('register-form');
  if (!form) return;

  // Role tabs
  const tabs = document.querySelectorAll('.role-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const role = tab.dataset.role;
      document.getElementById('student-fields').style.display = role === 'student' ? 'block' : 'none';
      document.getElementById('employer-fields').style.display = role === 'employer' ? 'block' : 'none';
    });
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Создаю аккаунт...';

    const role = document.querySelector('.role-tab.active')?.dataset.role || 'student';
    const body = {
      email:      form.email.value,
      password:   form.password.value,
      role,
      first_name: form.first_name.value,
      last_name:  form.last_name.value,
    };
    if (role === 'student') {
      body.specialty = form.specialty?.value || '';
      body.year      = parseInt(form.year?.value) || null;
    } else {
      body.organization = form.organization?.value || '';
      body.contact_name = form.first_name.value + ' ' + form.last_name.value;
    }

    try {
      await authAPI.register(body);
      const data = await authAPI.login({ email: body.email, password: body.password });
      setToken(data.access_token);
      const user = await authAPI.me();
      localStorage.setItem('uw_user', JSON.stringify(user));
      toast('Аккаунт создан!', 'success');
      setTimeout(() => window.location.href = 'index.html', 700);
    } catch (err) {
      toast(err.message, 'error');
      btn.disabled = false; btn.textContent = 'Зарегистрироваться';
    }
  });
}
