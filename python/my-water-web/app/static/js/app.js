function formatPhoneNumber(phone) {
    // Remove todos os caracteres que não sejam números
    phone = phone.replace(/\D/g, '');
  
    // Verifica se tem 11 dígitos (telefone com 9º dígito)
    if (phone.length === 11) {
      return phone.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
    }
    
    // Verifica se tem 10 dígitos (telefone fixo)
    else if (phone.length === 10) {
      return phone.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
    } else {
      return phone; // Retorna o número original se não tiver 10 ou 11 dígitos
    }
}

function formatCurrencyWithPrefix(value) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function formatCurrency(value) {
  return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function updateQuantityItens() {
  const quantity_items = sessionStorage.getItem('quantity_itens');
  if(quantity_items > 0) {
    counterCartShow(quantity_items);
  } else {
    counterCartHiden();
  }
  
}

function counterCartHiden() {
  var element = document.getElementById("cart-counter");

  element.style.display = "none";
  //element.className = element.className;
  //element.style = element.style;
}

function counterCartShow(quantity_items) {
  var element = document.getElementById("cart-counter");

  element.style.display = "block";
  element.innerText = quantity_items;
  
  //element.className = element.className;
  element.style = element.style;
}