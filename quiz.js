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
          <p class="why" hidden></p>
        </div>`).join('')}
      <button class="btn" id="check">Проверить</button>
      <button class="btn ghost" id="retry" hidden>Пройти тест заново</button>
      <p class="result" id="result"></p>
    </section>
    <nav class="pager">
      ${prev ? `<a href="${prev.id}.html">← ${prev.title}</a>` : ''}
      ${next ? `<a class="next" id="next" href="${next.id}.html">${next.title} ${arrow}</a>` : '<a class="next" id="next" href="../index.html">На главную</a>'}
    </nav>`);

  const result = document.getElementById('result');
  const check = document.getElementById('check'), retry = document.getElementById('retry');
  const inputs = [...document.querySelectorAll('.q input')];
  const qEls = [...document.querySelectorAll('.q')];

  // Темы разные, поэтому «дальше» открыт всегда: тест нужен для звезды, а не для пропуска вперёд.
  if (getDone().includes(id)) { result.textContent = 'Этот урок ты уже прошёл. Можно повторить!'; result.className = 'result ok'; }

  check.onclick = () => {
    const answers = questions.map((_, qi) => {
      const el = document.querySelector(`input[name=q${qi}]:checked`);
      return el ? Number(el.value) : null;
    });
    if (answers.includes(null)) { result.textContent = 'Ответь на все вопросы.'; result.className = 'result'; return; }
    const res = grade(questions, answers);
    qEls.forEach((el, qi) => {
      el.className = 'q ' + (res[qi] ? 'ok' : 'bad');
      const why = el.querySelector('.why');
      why.hidden = res[qi];
      if (!res[qi]) why.innerHTML = `<b>Правильно: ${questions[qi].a[questions[qi].right]}.</b> ${questions[qi].why || ''}`;
    });
    const right = res.filter(Boolean).length;
    if (right === questions.length) {
      const isNew = !getDone().includes(id);
      markDone(id);
      // Награды: звезда за новый урок, медаль, если этот урок закрыл мир, кубок, если закрыты все.
      const done = getDone();
      const worldDone = inSection.every(l => done.includes(l.id));
      const allDone = LESSONS.every(l => done.includes(l.id));
      const star = '<svg width="22" height="22" viewBox="0 0 24 24" fill="#ffd84d" stroke="#1c1f2e" stroke-width="2" stroke-linejoin="round" style="vertical-align:-4px"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>';
      const award = !isNew ? 'Урок пройден.'
        : allDone ? `${star} Новая звезда, медаль «${sec.title}» и кубок «Мастер компьютера»!`
        : worldDone ? `${star} Новая звезда и медаль «${sec.title}»!`
        : `${star} Новая звезда!`;
      result.innerHTML = `Всё верно! ${award} <a href="../index.html#awards">Мои награды</a>${next && !allDone ? ' · жми «дальше» внизу.' : ''}`;
      result.className = 'result ok';
    } else {
      // Ответы замораживаем: чтобы идти дальше, тест надо пройти заново целиком.
      inputs.forEach(i => i.disabled = true);
      check.hidden = true; retry.hidden = false;
      result.textContent = `Правильно ${right} из ${questions.length}. Прочитай объяснения под красными вопросами и пройди тест заново.`;
      result.className = 'result';
    }
  };

  retry.onclick = () => {
    inputs.forEach(i => { i.disabled = false; i.checked = false; });
    qEls.forEach(el => { el.className = 'q'; el.querySelector('.why').hidden = true; });
    retry.hidden = true; check.hidden = false;
    result.textContent = ''; result.className = 'result';
    document.getElementById('quiz').scrollIntoView({ behavior: 'smooth' });
  };
})();

if (typeof module !== 'undefined') module.exports = { grade };
