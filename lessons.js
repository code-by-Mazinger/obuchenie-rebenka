// Единственный список уроков. Добавил урок сюда и создал файл lessons/<id>.html — он появится везде.
const ICON = (d) => `<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${d}</svg>`;

const SECTIONS = [
  { id: 'win',     title: 'Windows',    color: '#2f6df6', desc: 'Компьютер, окна, файлы и папки',
    icon: ICON('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>') },
  { id: 'word',    title: 'Word',       color: '#4f46e5', desc: 'Пишем и оформляем тексты',
    icon: ICON('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M8 13h8M8 17h6"/>') },
  { id: 'excel',   title: 'Excel',      color: '#16a34a', desc: 'Таблицы, которые сами считают',
    icon: ICON('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16M15 4v16"/>') },
  { id: 'ppt',     title: 'PowerPoint', color: '#ea580c', desc: 'Делаем презентации',
    icon: ICON('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M12 16v5M8 21h8M7 12l3-3 2 2 4-4"/>') },
  { id: 'outlook', title: 'Outlook',    color: '#0ea5e9', desc: 'Электронная почта, календарь и дела',
    icon: ICON('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>') },
];

const LESSONS = [
  { id: 'w1', section: 'win',   title: 'Включаем компьютер и смотрим на рабочий стол' },
  { id: 'w2', section: 'win',   title: 'Мышь и клавиатура' },
  { id: 'w3', section: 'win',   title: 'Окна: открыть, свернуть, закрыть' },
  { id: 'w4', section: 'win',   title: 'Файлы и папки' },
  { id: 'w5', section: 'win',   title: 'Копировать, вставить, удалить' },
  { id: 'w6', section: 'win',   title: 'Меню Пуск и поиск программ' },
  { id: 'w7', section: 'win',   title: 'Правила безопасности' },

  { id: 'd1', section: 'word',  title: 'Первый документ: пишем и сохраняем' },
  { id: 'd2', section: 'word',  title: 'Жирный, курсив, размер и цвет' },
  { id: 'd3', section: 'word',  title: 'Списки и выравнивание' },
  { id: 'd4', section: 'word',  title: 'Картинки и таблицы' },
  { id: 'd5', section: 'word',  title: 'Печатаем и отправляем' },

  { id: 'e1', section: 'excel', title: 'Что такое таблица' },
  { id: 'e2', section: 'excel', title: 'Формулы: таблица считает сама' },
  { id: 'e3', section: 'excel', title: 'Рисуем диаграмму' },

  { id: 'p1', section: 'ppt',   title: 'Первая презентация' },
  { id: 'p2', section: 'ppt',   title: 'Картинки, оформление и переходы' },
  { id: 'p3', section: 'ppt',   title: 'Показываем презентацию' },

  { id: 'o1', section: 'outlook', title: 'Outlook: почта, календарь, контакты и задачи' },
];

// Прогресс хранится в браузере. localStorage может быть недоступен (приватное окно) — тогда просто ничего не помним.
function getDone() { try { return JSON.parse(localStorage.getItem('done') || '[]'); } catch { return []; } }
function markDone(id) { try { localStorage.setItem('done', JSON.stringify([...new Set([...getDone(), id])])); } catch {} }
