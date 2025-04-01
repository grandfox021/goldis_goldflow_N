<template>
  <q-page class="column flex-center">
    <q-spinner color="primary" size="3em" />
    <p>در حال ورود ...</p>
  </q-page>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "src/stores/auth";
import { api } from "src/boot/axios";

const router = useRouter();
const authStore = useAuthStore();

async function handleCallback() {
  try {
    await authStore.checkAuth();
    if (authStore.isAuthenticated) {
      const { data } = await api.get("/get-user-info");
      authStore.updateUserInfo(data.user_info);
      if(data.user_info.user_type === 2){
        localStorage.setItem('idType',data.user_info.user_type )
      }
      router.push("/dashboard");
    } else {
      const idpUrl = "http://localhost:9005/login";
      const redirectUri = "http://localhost:9000/authCallBack";
      const callbackUrl = "http://localhost:8080/auth/callback";
      window.location.href = `${idpUrl}?redirect_uri=${encodeURIComponent(redirectUri)}&callback_url=${encodeURIComponent(callbackUrl)}`;
    }
  } catch (error) {
    console.error("🔴 Authentication check failed:", error);
    router.push("/");
  }
}

handleCallback();
</script>
