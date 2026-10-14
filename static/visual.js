const main = document.querySelector('main');
const alphabet = JSON.parse(main.dataset.alfabeto);
const size = BigInt(alphabet.length);
const mod = (value) => Number(((value % size) + size) % size);
const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab) {
  tabs.forEach((item) => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
  });
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const next = tabs[event.key === 'Home' ? 0 : event.key === 'End' ? 1 : 1 - index];
    selectTab(next);
    next.focus();
  });
});
selectTab(document.getElementById('aba-' + main.dataset.aba));

const word = document.getElementById('palavra');
const shiftInput = document.getElementById('passos');
const range = document.getElementById('faixa');
const originals = document.getElementById('originais');
const animated = document.getElementById('animadas');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let previous = 0n;
let letters = [];
let animations = [];

function tile(character, className = 'letra') {
  const element = document.createElement('span');
  element.className = className;
  element.textContent = character === ' ' ? '␣' : character;
  return element;
}
function readShift() {
  if (!/^-?\d+$/.test(shiftInput.value)) return null;
  return BigInt(shiftInput.value);
}
function render(rebuild = false) {
  const shift = readShift();
  document.getElementById('erro-visual').hidden = shift !== null;
  if (shift === null) return;
  animations.forEach((animation) => animation.cancel());
  animations = [];
  if (rebuild) {
    letters = Array.from(word.value.normalize('NFC'));
    originals.replaceChildren(...letters.map((letter) => tile(letter)));
    animated.replaceChildren(...letters.map(() => tile('', 'letra janela')));
  }
  const difference = shift - previous;
  const direction = difference < 0n ? -1 : 1;
  const distance = difference < 0n ? -difference : difference;
  // Show at most one full turn plus the remainder, even for very large keys.
  const steps = Number(distance > size * 2n ? size + distance % size : distance);
  const result = letters.map((letter, index) => {
    const position = alphabet.indexOf(letter);
    const finalLetter = position < 0 ? letter : alphabet[mod(BigInt(position) + shift)];
    const windowElement = animated.children[index];
    windowElement.replaceChildren(tile(finalLetter, 'digito'));
    if (!rebuild && position >= 0 && steps && !reducedMotion.matches) {
      const reel = document.createElement('span');
      reel.className = 'rolo';
      for (let step = 0; step <= steps; step++) {
        const offset = direction > 0 ? step : steps - step;
        reel.append(tile(alphabet[mod(BigInt(position) + previous + BigInt(direction * offset))], 'digito'));
      }
      windowElement.replaceChildren(reel);
      const end = -steps * 100 / (steps + 1);
      const animation = reel.animate([
        { transform: 'translateY(' + (direction > 0 ? 0 : end) + '%)' },
        { transform: 'translateY(' + (direction > 0 ? end : 0) + '%)' }
      ], { duration: Math.min(1800, 420 + steps * 65), delay: index * 35, easing: 'cubic-bezier(.22,.7,.18,1)', fill: 'both' });
      animation.onfinish = () => {
        windowElement.replaceChildren(tile(finalLetter, 'digito'));
        animation.cancel();
      };
      animations.push(animation);
    }
    return finalLetter;
  }).join('');
  document.getElementById('saida-visual').textContent = result || '—';
  document.getElementById('indicador').textContent = shift === 0n ? '0 posições · sem deslocamento' : (shift > 0n ? '+' : '') + shift + (shift === 1n || shift === -1n ? ' posição' : ' posições') + (shift > 0n ? ' · avançar ↓' : ' · voltar ↑');
  range.value = String(shift > size - 1n ? size - 1n : shift < 1n - size ? 1n - size : shift);
  previous = shift;
}
word.addEventListener('input', () => render(true));
shiftInput.addEventListener('input', () => render());
range.addEventListener('input', () => { shiftInput.value = range.value; render(); });
for (const [id, delta] of [['diminuir', -1n], ['aumentar', 1n]]) {
  document.getElementById(id).addEventListener('click', () => {
    shiftInput.value = String((readShift() ?? previous) + delta);
    render();
  });
}
render(true);
