'use strict';

const button = document.querySelector('#add-item');
const form = document.querySelector('#add-item-form');
const table = document.querySelector('#walmart-goods');
const template = document.querySelector('#walmart-goods tr');

function addRow() {
    const row = template.cloneNode(true);
    row.querySelectorAll('input').forEach(input => input.value = '');
    table.appendChild(row);
}

button.addEventListener('click', addRow);

form.addEventListener('submit', (evt) => {
    evt.preventDefault();
    fetch('/proceed_order', {
        method: 'POST',
        body: new FormData(form)
    })
    .then(() => {
        window.location.href = '/result'; 
    });
});



