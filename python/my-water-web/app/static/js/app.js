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
  console.log( 'valor formatado: ', value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function formatCurrency(value) {
  return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}