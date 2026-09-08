// Запуск: node test.js
const assert = require('assert');
const { grade } = require('./quiz.js');

const qs = [{ q: 'a', a: ['x', 'y'], right: 1 }, { q: 'b', a: ['x', 'y'], right: 0 }];
assert.deepStrictEqual(grade(qs, [1, 0]), [true, true]);
assert.deepStrictEqual(grade(qs, [0, 0]), [false, true]);
assert.deepStrictEqual(grade(qs, [null, 1]), [false, false]);
console.log('ok');
