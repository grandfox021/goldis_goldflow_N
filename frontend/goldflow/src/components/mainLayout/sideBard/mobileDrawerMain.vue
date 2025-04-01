<template>
    <q-drawer
      bordered
      class="mobile-drawer"
      :width="280"
    >
      <q-scroll-area class="fit">
        <div class="drawer-header q-pa-md">
          <img
            :src="logo"
            alt="Goldis Logo"
            class="drawer-logo"
          />
        </div>

        <q-list padding>
          <q-item
            v-for="(item, index) in navigationItems"
            :key="index"
            :to="item.route"
            clickable
            v-ripple
            class="drawer-item"
          >
            <q-item-section>{{ item.label }}</q-item-section>
          </q-item>

          <q-separator class="q-my-md" />

          <!-- Mobile Auth Buttons -->
          <q-item>
            <q-item-section>
              <div v-if="!isAuthenticated" class="column q-gutter-y-sm">
                <q-btn
                  unelevated
                  color="primary"
                  label="ورود"
                  class="drawer-btn"
                  @click="redirectToLogin"
                />
                <q-btn
                  outline
                  color="secondary"
                  label="ثبت نام"
                  class="drawer-btn"
                  @click="redirectToSingUp"
                />
              </div>
              <div v-else class="column q-gutter-y-sm">
                <q-btn
                  unelevated
                  color="primary"
                  label="ورود"
                  class="drawer-btn"
                  @click="router.push('/dashboard')"
                />
              </div>
            </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>
    </q-drawer>
</template>

<script setup>
import { computed } from 'vue';
import logo from '../../../assets/LOGO.png'
import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router';

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated ? true : false)

const navigationItems = [
  { label: "خانه", route: "/" },
  { label: "درباره ما", route: "/about" },
  { label: "تماس با ما", route: "/contact" },
  { label: "مجله", route: "/blog" },
];

function redirectToLogin() {
  const idpUrl = "http://localhost:9005/login";
  const redirectUri = "http://localhost:9000/authCallBack";
  const callbackUrl = "http://localhost:8080/auth/callback";
  window.location.href = `${idpUrl}?redirect_uri=${encodeURIComponent(redirectUri)}&callback_url=${encodeURIComponent(callbackUrl)}`;
}

function redirectToSingUp() {
  console.log("Redirecting to signup...");
  const idpUrl = "http://localhost:9005/signup";
  const redirectUri = "http://localhost:9000/authCallBack";
  const callbackUrl = "http://localhost:8080/auth/callback";
  window.location.href = `${idpUrl}?redirect_uri=${encodeURIComponent(redirectUri)}&callback_url=${encodeURIComponent(callbackUrl)}`;
}
</script>

<style scoped>
.mobile-drawer {
  background: white;
}
.drawer-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 24px;
}

.drawer-logo {
  height: 36px;
  object-fit: contain;
}

.drawer-item {
  border-radius: 8px;
  margin: 4px 0;
  transition: background-color 0.3s ease;
}

.drawer-item:hover {
  background: rgba(var(--q-primary-rgb), 0.05);
}
</style>
