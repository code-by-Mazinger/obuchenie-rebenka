// node test.js — проверка логики теста и целостности курса. Ничего не меняет.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = __dirname;
const read = p => fs.readFileSync(path.join(root, p), 'utf8');

// 1. Проверка ответов в уроке
const { grade } = require('./quiz.js');
const qs = [{ right: 1 }, { right: 0 }, { right: 2 }];
assert.deepStrictEqual(grade(qs, [1, 0, 2]), [true, true, true]);
assert.deepStrictEqual(grade(qs, [1, 1, 2]), [true, false, true]);
assert.deepStrictEqual(grade(qs, [null, 0, 2]), [false, true, true]);

// 2. Подсчёт и уровень в отдельных тестах (входном и итоговом)
const { scoreExam, examLevel } = require('./exam.js');
const examQs = [
  { right: 0, section: 'win' }, { right: 1, section: 'win' },
  { right: 2, section: 'ai' }, { right: 0, section: 'word' }
];
const scored = scoreExam(examQs, [0, 0, 2, 1]);
assert.strictEqual(scored.count, 2);
assert.deepStrictEqual(scored.weak, { win: 1, word: 1 }, 'Слабые миры считаются по ошибкам');
const levels = [{ min: 0, title: 'низкий' }, { min: 0.5, title: 'средний' }, { min: 0.9, title: 'высокий' }];
assert.strictEqual(examLevel(levels, 0, 4).title, 'низкий');
assert.strictEqual(examLevel(levels, 2, 4).title, 'средний');
assert.strictEqual(examLevel(levels, 4, 4).title, 'высокий');

// 3. Каждый урок из списка существует, размечен своим id и несёт рабочий тест
const { LESSONS, SECTIONS, lessonsWord, lessonsOf, plural } = vm.runInNewContext(read('lessons.js') + ';({ LESSONS, SECTIONS, lessonsWord, lessonsOf, plural })');

const sectionIds = new Set(SECTIONS.map(s => s.id));
for (const lesson of LESSONS) {
  assert.ok(sectionIds.has(lesson.section), `Урок ${lesson.id}: неизвестный раздел ${lesson.section}`);
  const file = `lessons/${lesson.id}.html`;
  assert.ok(fs.existsSync(path.join(root, file)), `Нет файла урока: ${file}`);
  const html = read(file);
  assert.ok(html.includes(`data-lesson="${lesson.id}"`), `${file}: в body нет data-lesson="${lesson.id}"`);
  const quiz = /<script type="application\/json" id="quiz-data">([\s\S]*?)<\/script>/.exec(html);
  assert.ok(quiz, `${file}: нет блока quiz-data`);
  const questions = JSON.parse(quiz[1]);
  assert.ok(questions.length >= 3, `${file}: в тесте меньше трёх вопросов`);
  questions.forEach((q, i) => {
    assert.ok(q.q && Array.isArray(q.a) && q.a.length >= 2, `${file}, вопрос ${i + 1}: нет текста или вариантов`);
    assert.ok(Number.isInteger(q.right) && q.right >= 0 && q.right < q.a.length, `${file}, вопрос ${i + 1}: неверный номер правильного ответа`);
    assert.ok(q.why, `${file}, вопрос ${i + 1}: нет объяснения why`);
  });
  const img = /<main>[\s\S]*?<img src="\.\.\/img\/([^"]+)"/.exec(html);
  if (img) assert.ok(fs.existsSync(path.join(root, 'img', img[1])), `${file}: нет картинки img/${img[1]}`);
}

// 4. Склонение числа уроков
assert.strictEqual(lessonsWord(1), 'урок');
assert.strictEqual(lessonsWord(24), 'урока');
assert.strictEqual(lessonsWord(11), 'уроков');
assert.strictEqual(lessonsWord(19), 'уроков');
assert.strictEqual(lessonsOf(24), 'уроков');
assert.strictEqual(lessonsOf(21), 'урока');
assert.strictEqual(lessonsOf(11), 'уроков');
assert.strictEqual(plural(6, 'мир', 'мира', 'миров'), 'миров');
assert.strictEqual(plural(2, 'мир', 'мира', 'миров'), 'мира');

console.log(`ok: ${LESSONS.length} ${lessonsWord(LESSONS.length)} в ${SECTIONS.length} мирах, тесты уроков и отдельные тесты проверены`);
