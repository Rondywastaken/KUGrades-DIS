document.querySelectorAll('[data-course-search]').forEach((root) => {
  const input = root.querySelector('[data-search-input]');
  const dropdown = root.querySelector('[data-search-dropdown]');
  if (!input || !dropdown) return;

  let timer;

  input.addEventListener('input', () => {
    clearTimeout(timer);
    const q = input.value.trim();
    if (q.length < 2) {
      dropdown.classList.add('hidden');
      return;
    }
    timer = setTimeout(async () => {
      const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      dropdown.innerHTML = '';
      if (!data.length) {
        dropdown.classList.add('hidden');
        return;
      }
      data.forEach((course) => {
        const li = document.createElement('li');
        li.innerHTML = `<span class="dd-code">${course.id}</span><span class="dd-name">${course.name}</span>`;
        li.addEventListener('mousedown', () => {
          window.location.href = `/course/${course.id}`;
        });
        dropdown.appendChild(li);
      });
      dropdown.classList.remove('hidden');
    }, 200);
  });

  document.addEventListener('click', (e) => {
    if (!root.contains(e.target)) dropdown.classList.add('hidden');
  });

  input.addEventListener('focus', () => {
    if (dropdown.children.length) dropdown.classList.remove('hidden');
  });
});
