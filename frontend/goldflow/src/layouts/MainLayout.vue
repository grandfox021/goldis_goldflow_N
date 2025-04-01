<template>
  <q-layout view="lHh Lpr lFf">
    <q-header class="header-main bg-info">
      <q-toolbar class="container">
        <!-- Mobile Menu Button -->
        <q-btn
          flat
          dense
          round
          icon="menu"
          class="lt-md menu-button text-accent"
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
        />

        <div class="full-width custom-style flex items-center justify-between">
          <!-- right Section: Logo and Navigation -->
          <div class="flex flex-center">
            <!-- Logo with enhanced hover effect -->
            <q-btn
              flat
              no-caps
              class="logo-wrapper"
              @click="router.push('/')"
              aria-label="Home"
            >
              <img
                :src="logo"
                alt="Goldis Logo"
                class="nav-logo"
              />
            </q-btn>

            <q-separator vertical color="grey-3" class="gt-sm separator" />

            <!-- Desktop Navigation -->
            <div class="row q-gutter-x-md gt-sm nav-links">
              <sideBarMain />
            </div>
          </div>

          <!-- left Section: Auth Buttons -->
          <div v-if="!isAuthenticated" class="row items-center q-gutter-x-md auth-btn">
            <q-btn
              unelevated
              color="primary"
              label="ورود"
              class="auth-btn login-btn"
              @click="redirectToLogin"
            />
            <q-btn
              outline
              color="secondary"
              label="ثبت نام"
              class="auth-btn signup-btn"
              @click="redirectToSingUp"
            />

          </div>
          <div v-else class="items-center  auth-btn">
            <q-btn
                  unelevated
                  color="primary"
                  label="ورود"
                  class="drawer-btn"
                  @click="router.push('/dashboard')"
                />
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <!-- drawerrr  -->
    <mobileDrawerMain v-model="leftDrawerOpen"/>

    <q-page-container class="bg-info custom-padding">
        <router-view />
    </q-page-container>
    <footer-component />
  </q-layout>
</template>

<script setup>
import { defineAsyncComponent, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "src/stores/auth";
import logo from 'src/assets/LOGO.png'

const sideBarMain = defineAsyncComponent(() => import('../components/mainLayout/sideBard/sideBarMain.vue'))
const mobileDrawerMain = defineAsyncComponent(() => import('../components/mainLayout/sideBard/mobileDrawerMain.vue'))
const FooterComponent = defineAsyncComponent(() => import('../components/mainLayout/FooterComponent.vue'))


const router = useRouter();
const leftDrawerOpen = ref(false);
const isAuthenticated = ref(false);
const authStore = useAuthStore()


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
onMounted(() => {
  if(authStore.isAuthenticated){
    isAuthenticated.value = true
  }else{
    isAuthenticated.value = false
  }
})
</script>

<style scoped>
/* Header Styles */
.header-main {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.header-main:hover {
  background: rgba(255, 255, 255, 0.95);
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  height: 80px;
  padding: 0 24px;
}

/* Logo Styles */
.logo-wrapper {
  padding: 8px 16px;
  border-radius: 12px;
  transition: background-color 0.3s ease;
}

.logo-wrapper:hover {
  background: rgba(var(--q-primary-rgb), 0.05);
}

.nav-logo {
  height: 44px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.logo-wrapper:hover .nav-logo {
  transform: scale(1.05);
}

/* Auth Buttons */
.auth-btn {
  gap: 12px;
}

.auth-btn {
  min-width: 120px;
  height: 44px;
  font-weight: 500;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.login-btn {
  background: var(--q-primary);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--q-primary-rgb), 0.2);
}

.signup-btn:hover {
  transform: translateY(-2px);
  background: rgba(var(--q-secondary-rgb), 0.05);
}

/* Mobile Menu Button */
.menu-button {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  margin-left: 12px;
  background: rgba(var(--q-primary-rgb), 0.05);
}

/* Separator */
.separator {
  margin: 0 24px;
}



.drawer-btn {
  height: 48px;
  border-radius: 12px;
  font-weight: 500;
  width: 100%;
}


/* Remove default shadows */
:deep(.q-layout__shadow:after),
:deep(.q-layout__shadow:before) {
  box-shadow: none !important;
}

/* Responsive Adjustments */
@media (max-width: 1024px) {
  .container {
    padding: 0 16px;
  }

  .nav-links {
    margin-right: 16px;
  }

  .auth-btn {
    min-width: 100px;
  }
}

@media (max-width: 599px) {
  .container {
    height: 70px;
  }

  .nav-logo {
    height: 36px;
  }

  .auth-btn {
    display: none;
  }
  .custom-style{
    display: flex;
    flex-direction: row-reverse;
  }
}
.custom-padding{
  padding-bottom: 0 !important;
}
</style>
