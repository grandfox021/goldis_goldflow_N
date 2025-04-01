import { defineBoot } from "@quasar/app-vite/wrappers";
import { useAuthStore } from "src/stores/auth";
import { api } from "./axios";



export default defineBoot(async ({ router }) => {
  const authStore = useAuthStore();
  const idpUrl = 'http://localhost:9005/login';
  const redirectUri = 'http://localhost:9000/authCallBack';
  const callbackUrl = 'http://localhost:8080/auth/callback';


  if (!authStore.isInitialized) {
    await authStore.checkAuth();
  }

  if (authStore.isAuthenticated) {
    try {
      const { data } = await api.get("/get-user-info");
      authStore.updateUserInfo(data.user_info);
    } catch (error) {
      console.error("Failed to fetch user info:", error);
    }
  }

  router.beforeEach(async(to, from, next) => {
    if(!authStore.isInitialized){
      await authStore.checkAuth()
    }

    if(to.meta.public){
      return next()
    }

    if(authStore.isAuthenticated){
      next()
    }else{
      window.location.href = `${idpUrl}?redirect_uri=${encodeURIComponent(redirectUri)}&callback_url=${encodeURIComponent(callbackUrl)}`;
    }

  })
});
