import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "src/boot/axios";


export const useAuthStore = defineStore('auth',() => {
  const isAuthenticated = ref(false);
  const phoneNumber = ref(null);
  const password = ref('');
  const firstName = ref('');
  const lastName = ref('');
  const nationalId = ref('');
  const email = ref('')
  const isInitialized = ref(false);
  const userId = ref('')
  const rialBalance = ref('')
  const goldBalance = ref('')

  const checkAuth = async () => {
    try {
      const { data } = await api.get('/protected-resource');

      if (data.authenticated) {
        isAuthenticated.value = true;
      } else {
        isAuthenticated.value = false;
        clearUserInfo();
      }

      isInitialized.value = true;
    } catch (error) {
      console.error('🔴 Authentication check failed:', error);
      isAuthenticated.value = false;
      clearUserInfo();

      isInitialized.value = false;
    }
  };




  const updateUserInfo = (userData) => {
    firstName.value = userData.first_name || '';
    lastName.value = userData.last_name || '';
    password.value = userData.password || '';
    phoneNumber.value = userData.phone_number || '';
    nationalId.value = userData.national_id || '';
    userId.value = userData.id || '';
    rialBalance.value = userData.rial_balance || '';
    goldBalance.value = userData.gold_balance || '';
    email.value = userData.email || '';
  };

  const clearUserInfo = () => {
    firstName.value = '';
    lastName.value = '';
    password.value = '';
    phoneNumber.value =  '';
    nationalId.value = '';
    userId.value ='';
    rialBalance.value = '';
    goldBalance.value = '';
    email.value ='';
    isAuthenticated.value = false;
  };

  const logout = async () => {
    try {
      await api.post('/logout');
      localStorage.clear()
    } catch (error) {
      console.error('🚨 Logout error:', error);
    } finally {
      isAuthenticated.value = false;
      isInitialized.value = false;
      clearUserInfo();
    }
  };


  return {
    isAuthenticated,
    firstName,
    lastName,
    phoneNumber,
    password,
    userId,
    checkAuth,
    logout,
    updateUserInfo,
    clearUserInfo
  }
})
