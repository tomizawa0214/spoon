'use strict';

const size = [280, 330, 440];
const option = [50, 50];

function total_fee() {
    let size_total = 0;
    let option_total = 0;
    const total = document.getElementById('total_price');
    const flavor = document.getElementById('flavor');
    const flavor_2 = document.getElementById('flavor_2');
    const option_title = document.getElementById('option_title');
    const option_price = document.getElementById('option_price');
    const option_title_2 = document.getElementById('option_title_2');
    const option_price_2 = document.getElementById('option_price_2');
    const sizeform = document.getElementsByName('size')
    const flavorform = document.getElementsByName('flavor')
    const optionform = document.getElementsByName('option')

    for ( let i = 0; i < size.length; i++ ) {
        if ( sizeform[i].checked ) {
            let size_value = sizeform[i].value.split(' ');
            document.getElementById('size_title').textContent = size_value[0];
            document.getElementById('size_price').textContent = size_value[1];
            size_total = size[i];
        }
        total.textContent = size_total;
    }

    flavor.textContent = '';
    flavor_2.textContent = '';
    for ( let j = 0; j < 3; j++ ) {
        if ( flavorform[j].checked ) {
            let flavor_value = flavorform[j].value;
            if ( flavor.textContent == '' && flavor_2.textContent == '' ) {
                flavor.textContent = flavor_value;
            } else if ( flavor_2.textContent == '' ) {
                flavor_2.textContent = flavor_value;
            }
        }
    }

    option_title.textContent = '';
    option_price.textContent = '';
    option_title_2.textContent = '';
    option_price_2.textContent = '';
    for ( let k = 0; k < option.length; k++ ) {
        if ( optionform[k].checked ) {
            const option_value = optionform[k].value.split(' ');
            if ( k == 0 ) {
                option_title.textContent = option_value[0];
                option_price.textContent = option_value[1];
            } 
            if ( k == 1 ) {
                option_title_2.textContent = option_value[0];
                option_price_2.textContent = option_value[1];
            }
            option_total += option[k];
        }
        total.textContent = option_total;
    }
    total.textContent = size_total + option_total;
}