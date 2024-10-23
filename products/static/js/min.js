const bar = document.getElementById('bar');
const close = document.getElementById('close');
const navi = document.getElementById('dotdot');


if (bar) {
    bar.addEventListener('click', () => {
        navi.classList.add('active')
   
    })
}
if (close) {
    close.addEventListener('click', () => {
        navi.classList.remove('active')
   
    })
}