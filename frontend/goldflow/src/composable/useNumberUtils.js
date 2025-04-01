function persianToEnglish(input) {
  const persianDigits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
  const englishDigits = ['0','1','2','3','4','5','6','7','8','9'];
  let output = input;
  persianDigits.forEach((pd, i) => {
    output = output.replace(new RegExp(pd, 'g'), englishDigits[i]);
  });
  return output;
}


function englishToPersian(input){
  const persianDigits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
  const englishDigits = ['0','1','2','3','4','5','6','7','8','9'];
  let output = input;
  englishDigits.forEach((ed , i) => {
    output = output.replace(new RegExp(ed , 'g'), persianDigits[i]);
  });
  return output;
}

export {persianToEnglish , englishToPersian}
