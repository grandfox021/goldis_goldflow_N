import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "src/boot/axios";

export const useWalletStore = defineStore('wallet', () => {
  const balance = ref(122342343);
  const goldAmount = ref(1)
  const price = ref(6550000);

  let intervalId = null;

  const checkPrice = async () => {
    if (intervalId) return;

    try {
      const { data } = await api.get('/get-gold-current-price');
      price.value = data.gold_current_price/ 10;
    } catch (error) {
      console.error("Error fetching price:", error);
    }

    intervalId = setInterval(async () => {
      try {
        const { data } = await api.get('/get-gold-current-price');
        price.value = data.gold_current_price / 10;
      } catch (error) {
        console.error("Error fetching price:", error);
      }
    }, 600000);
  };


  const setBalance = async() => {
    try{
      const { data } = await api.get('get-user-info')
      balance.value = Math.round(data.user_info.rial_balance);
    }catch(err){
      console.log(err)
    }
  }


  const setGoldAmount = async() => {
    try{
      const { data } = await api.get('get-user-info')
      goldAmount.value = data.user_info.gold_balance
    }catch(err){
      console.log(err)
    }
  }


  return { balance, price,goldAmount, setBalance, checkPrice, setGoldAmount };
});
