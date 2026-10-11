const links = document.querySelectorAll('nav a');
const secs = [...document.querySelectorAll('section')];
function spy() {
  let cur = secs[0].id;
  for (const s of secs) if (s.getBoundingClientRect().top < window.innerHeight * 0.35) cur = s.id;
  links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + cur));
}
addEventListener('scroll', spy, { passive: true }); spy();
document.querySelectorAll('details nav a').forEach(a => a.addEventListener('click', () => a.closest('details').open = false));

const url = location.origin + location.pathname, title = document.title;
document.getElementById('share-x').href = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodeURIComponent(url);
document.getElementById('share-li').href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url);
const copy = document.getElementById('copy-link');
copy.onclick = () => navigator.clipboard.writeText(url).then(() => { copy.textContent = 'Copied!'; setTimeout(() => copy.textContent = 'Copy link', 1800); });
if (navigator.share) { const n = document.getElementById('native-share'); n.hidden = false; n.onclick = () => navigator.share({ title, url }).catch(() => {}); }

const box = document.getElementById('comments');
const base = document.currentScript.src.replace(/post\.js.*$/, '');
const mode = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
const g = document.createElement('script');
g.src = 'https://giscus.app/client.js'; g.async = true; g.crossOrigin = 'anonymous';
const a = { 'data-repo': 'Dead-Bytes/blogs', 'data-repo-id': 'R_kgDOVEf27Q', 'data-category': 'Announcements', 'data-category-id': 'DIC_kwDOVEf27c4DHj9Y',
  'data-mapping': 'specific', 'data-term': box.dataset.term, 'data-strict': '1', 'data-reactions-enabled': '1',
  'data-emit-metadata': '0', 'data-input-position': 'top', 'data-theme': base + 'giscus-' + mode + '.css', 'data-lang': 'en', 'data-loading': 'lazy' };
for (const k in a) g.setAttribute(k, a[k]);
box.appendChild(g);
