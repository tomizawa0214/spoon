const stripe = Stripe('pk_test_nxX8t5nHgIQGkdFQmby1vkiB00v6lis7lO');
const elements = stripe.elements();

const style = {
  base: {
    fontSize: '16px',
    color: '#32325d',
  },
  invalid: { //値が不正のときに文字色を変える
    color: '#f00',
    iconColor: '#f00'
  }
};

// フォームのidを指定してElementsをマウント
const cardNumber = elements.create('cardNumber', {
  style: style,
  placeholder: '0000 0000 0000 0000'
});
cardNumber.mount('#card-number');

const cardExpiry = elements.create('cardExpiry',{
  style: style,
  placeholder: '00/00'
});
cardExpiry.mount('#card-expiry');

const cardCvc = elements.create('cardCvc', {
  style: style,
  placeholder: '000'
});
cardCvc.mount('#card-cvc');

// カード番号のリアルタイムバリデーション
const toggle = [cardNumber, cardExpiry, cardCvc];
for (let i = 0; i < toggle.length; i++) {
  toggle[i].addEventListener('change', function (event) {
    const displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });
}

// 確定ボタンでエラーをチェック
const form = document.getElementById('payment-form');
form.addEventListener('submit', function (event) {
  event.preventDefault();

  stripe.createToken(cardNumber, cardExpiry, cardCvc).then(function (result) {
    if (result.error) {
      const errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      stripeTokenHandler(result.token);
    }
  });
});

// フォーム送信処理 (stripeTokenをhiddenで送信)
function stripeTokenHandler(token) {
  const form = document.getElementById('payment-form');
  const hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);
  form.submit();
}