const API = 'http://127.0.0.1:8000';

function getToken() { return localStorage.getItem('uw_token'); }
function setToken(t) { localStorage.setItem('uw_token', t); }
function removeToken() { localStorage.removeItem('uw_token'); localStorage.removeItem('uw_user'); }

function authHeaders() {
  const t = getToken();
  return t ? { 'Authorization': `Bearer ${t}`, 'Content-Type': 'application/json' }
           : { 'Content-Type': 'application/json' };
}

async function request(method, path, body = null) {
  const opts = { method, headers: authHeaders() };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(API + path, opts);
  const data = await res.json();
  if (!res.ok) {
    const msg = data?.error?.message || data?.detail || 'Ошибка запроса';
    throw new Error(msg);
  }
  return data;
}

/* Auth */
const authAPI = {
  register: (body) => request('POST', '/api/auth/register', body),
  login:    (body) => request('POST', '/api/auth/login', body),
  me:       ()     => request('GET',  '/api/auth/me'),
};

/* Jobs */
const jobsAPI = {
  list:   (params = {}) => {
    const q = new URLSearchParams(Object.fromEntries(Object.entries(params).filter(([,v]) => v)));
    return request('GET', `/api/jobs/?${q}`);
  },
  get:    (id)   => request('GET',   `/api/jobs/${id}`),
  create: (body) => request('POST',  '/api/jobs/', body),
  close:  (id)   => request('PATCH', `/api/jobs/${id}/close`),
};

/* Applications */
const appsAPI = {
  apply:      (body)         => request('POST',  '/api/applications/', body),
  my:         ()             => request('GET',   '/api/applications/my'),
  forJob:     (jobId)        => request('GET',   `/api/applications/job/${jobId}`),
  setStatus:  (id, status)   => request('PATCH', `/api/applications/${id}/status`, { status }),
};

/* Categories */
const catsAPI = {
  list: () => request('GET', '/api/categories/'),
};

/* Notifications */
const notifsAPI = {
  list: () => request('GET', '/api/users/notifications'),
};
