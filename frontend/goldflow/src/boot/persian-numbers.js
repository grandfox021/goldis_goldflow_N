export default ({ app }) => {
  // Global Mixin to replace all numbers in text content
  app.mixin({
    mounted() {
      this.replaceNumbers();
    },
    updated() {
      this.replaceNumbers();
    },
    methods: {
      replaceNumbers() {
        const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
        const convertToPersianNumbers = value => value.replace(/\d/g, digit => persianDigits[digit]);

        this.$nextTick(() => {
          const elements = document.body.querySelectorAll('*:not(script):not(style)');
          elements.forEach(el => {
            el.childNodes.forEach(node => {
              if (node.nodeType === 3 && /\d/.test(node.nodeValue)) {
                node.nodeValue = convertToPersianNumbers(node.nodeValue);
              }
            });
          });
        });
      }
    }
  });

  // Directive for input fields
  app.directive('persian-numbers', {
    beforeMount(el) {
      el.addEventListener('input', event => {
        const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
        const convertToPersianNumbers = value => value.replace(/\d/g, digit => persianDigits[digit]);

        const inputValue = event.target.value;
        const newValue = convertToPersianNumbers(inputValue);
        if (newValue !== inputValue) {
          event.target.value = newValue;
          event.target.dispatchEvent(new Event('input'));
        }
      });
    }
  });
};
