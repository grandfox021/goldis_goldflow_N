function validationNumber(value){
  return !!value || 'شماره موبایل الزامی است'
}
function validateInput(val) {
  return !!val || 'نباید خالی باشد';
}

export{validationNumber,validateInput}



