// Общий движок для отдельных тестов: входного (entry.html) и итогового (final.html).
// Страница задаёт EXAM = { kind, title, lead, questions, levels } и вызывает runExam().
// Вопрос: { q, a: [...], right, section } — section нужен, чтобы посчитать слабые миры.
// Прогресс уроков тесты НЕ меняют: они только показывают результат и советуют, куда идти.

function scoreExam(questions, answers) {
  const right = questions.map((q, i) => answers[i] === q.right);
  const weak = {};
  questions.forEach((q, i) => {
    if (!right[i] && q.section) weak[q.section] = (weak[q.section] || 0) + 1;
  });
  return { right, count: right.filter(Boolean).length, weak };
}

function examLevel(levels, count, total) {
  // levels: [{ min, title, text }] — от меньшего к большему, берём последний подходящий
  const share = total ? count / total : 0;
  return levels.reduce((found, level) => (share >= level.min ? level : found), levels[0]);
}

if (typeof document !== 'undefined') (function () {
  const exam = window.EXAM;
  const wrap = document.querySelector('main');

  document.title = exam.title + ' — Учимся с компьютером';
  document.body.classList.add('lesson', 'wrap');
  document.querySelector('header').className = 'top';
  document.querySelector('header').innerHTML =
    `<a href="index.html">← Все уроки</a><span class="pill c">${exam.badge}</span>`;

  wrap.insertAdjacentHTML('beforeend', `
    <section class="quiz" id="exam">
      <h2>${exam.heading}</h2>
      ${exam.questions.map((q, qi) => `
        <div class="q" data-q="${qi}">
          <p><b>${qi + 1}. ${q.q}</b></p>
          ${q.a.map((a, ai) => `<label><input type="radio" name="q${qi}" value="${ai}"> ${a}</label>`).join('')}
        </div>`).join('')}
      <button class="btn" id="check">Показать результат</button>
      <button class="btn ghost" id="retry" hidden>Пройти заново</button>
      <div class="exam-result" id="result" hidden></div>
    </section>
    <nav class="pager"><a href="index.html">← На главную</a></nav>`);

  const result = document.getElementById('result');
  const check = document.getElementById('check');
  const retry = document.getElementById('retry');
  const qEls = [...document.querySelectorAll('.q')];

  check.onclick = () => {
    const answers = exam.questions.map((_, qi) => {
      const el = document.querySelector(`input[name=q${qi}]:checked`);
      return el ? Number(el.value) : null;
    });
    if (answers.includes(null)) {
      result.hidden = false;
      result.innerHTML = '<p class="result">Ответь на все вопросы.</p>';
      return;
    }
    const { right, count, weak } = scoreExam(exam.questions, answers);
    qEls.forEach((el, qi) => { el.className = 'q ' + (right[qi] ? 'ok' : 'bad'); });
    const level = examLevel(exam.levels, count, exam.questions.length);
    const weakest = Object.entries(weak).sort((a, b) => b[1] - a[1]).map(([id]) => id);
    const advice = exam.advice(weakest, count);
    result.hidden = false;
    result.innerHTML =
      `<p class="result ok">Правильно ${count} из ${exam.questions.length}</p>` +
      `<h3>${level.title}</h3><p>${level.text}</p>${advice}`;
    check.hidden = true;
    retry.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  retry.onclick = () => {
    document.querySelectorAll('.q input').forEach(i => { i.checked = false; });
    qEls.forEach(el => { el.className = 'q'; });
    result.hidden = true;
    retry.hidden = true;
    check.hidden = false;
    document.getElementById('exam').scrollIntoView({ behavior: 'smooth' });
  };
})();

if (typeof module !== 'undefined') module.exports = { scoreExam, examLevel };
