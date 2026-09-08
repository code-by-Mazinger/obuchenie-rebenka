// Подключается в конце каждого урока. Рисует шапку, тест и кнопки «назад/дальше».
// Урок должен иметь <body data-lesson="id"> и <script id="quiz-data" type="application/json">[...]</script>.

// Чистая функция: какие ответы верные. answers[i] — номер выбранного варианта или null.
function grade(questions, answers) {
  return questions.map((q, i) => answers[i] === q.right);
}

if (typeof document !== 'undefined') (function () {
  const id = document.body.dataset.lesson;
  const idx = LESSONS.findIndex(l => l.id === id);
  const lesson = LESSONS[idx];
  const sec = SECTIONS.find(s => s.id === lesson.section);
  const inSection = LESSONS.filter(l => l.section === lesson.section);
  const num = inSection.indexOf(lesson) + 1;
  const prev = LESSONS[idx - 1], next = LESSONS[idx + 1];

  document.title = lesson.title + ' — Учимся с компьютером';
  document.body.style.setProperty('--c', sec.color);
  document.body.classList.add('lesson', 'wrap');
  document.querySelector('header').className = 'top';
  document.querySelector('header').innerHTML =
    `<a href="../index.html">← Все уроки</a><span class="pill c">${sec.icon} ${sec.title} · урок ${num} из ${inSection.length}</span>`;

  const questions = JSON.parse(document.getElementById('quiz-data').textContent);
  const main = document.querySelector('main');
  const arrow = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

  main.insertAdjacentHTML('beforeend', `
    <section class="quiz" id="quiz">
      <h2>Проверь себя</h2>
      ${questions.map((q, qi) => `
        <div class="q" data-q="${qi}">
          <p><b>${qi + 1}. ${q.q}</b></p>
          ${q.a.map((a, ai) => `<label><input type="radio" name="q${qi}" value="${ai}"> ${a}</label>`).join('')}
        </div>`).join('')}
      <button class="btn" id="check">Проверить</button>
      <p class="result" id="result"></p>
    </section>
    <nav class="pager">
      ${prev ? `<a href="${prev.id}.html">← ${prev.title}</a>` : ''}
      ${next ? `<a class="next" href="${next.id}.html">${next.title} ${arrow}</a>` : '<a class="next" href="../index.html">На главную</a>'}
    </nav>`);

  const result = document.getElementById('result');
  if (getDone().includes(id)) { result.textContent = 'Этот урок ты уже прошёл. Можно повторить!'; result.className = 'result ok'; }

  document.getElementById('check').onclick = () => {
    const answers = questions.map((_, qi) => {
      const el = document.querySelector(`input[name=q${qi}]:checked`);
      return el ? Number(el.value) : null;
    });
    if (answers.includes(null)) { result.textContent = 'Ответь на все вопросы.'; result.className = 'result'; return; }
    const res = grade(questions, answers);
    document.querySelectorAll('.q').forEach((el, qi) => el.className = 'q ' + (res[qi] ? 'ok' : 'bad'));
    const right = res.filter(Boolean).length;
    if (right === questions.length) {
      markDone(id);
      result.textContent = `Всё верно! Урок пройден.${next ? ' Жми «дальше» внизу.' : ' Ты прошёл все уроки!'}`;
      result.className = 'result ok';
    } else {
      result.textContent = `Правильно ${right} из ${questions.length}. Красные вопросы — перечитай урок и попробуй ещё раз.`;
      result.className = 'result';
    }
  };
})();

if (typeof module !== 'undefined') module.exports = { grade };
