<template>
  <q-layout view="lHh Lpr lFf">
    <div class="main-container q-mb-md">
      <!-- Enhanced Gradient Background -->
      <div class="background-pattern">
        <div class="animated-waves"></div>
        <div class="gradient-overlay"></div>
      </div>
      <!--  Header -->
      <header class="header-section q-px-lg q-pt-md">
        <div class="row justify-between items-center q-pb-xl">
          <!-- barc menu  -->
          <div class="lt-md">

            <q-btn
              icon="menu"
              flat
              color="info"
              class="lt-md"
              @click="rightDrawerOpen = !rightDrawerOpen"
              aria-label="Menu"
            />
            <!-- mobile drawer  -->
            <drawerDashboard v-model="rightDrawerOpen" />

          </div>
          <!-- icon && logo  -->
          <div class="text-h4 flex flex-center items-center">
            <q-avatar size="48px" class="q-mr-md shadow-2">
              <img :src="favicon" alt="logo" />
            </q-avatar>
            <span class="text-weight-medium text-info q-pa-sm text-glow"
              >گلدیس</span
            >
          </div>

            <!-- Enhanced User Menu -->
          <div class="row items-center q-gutter-x-md gt-sm">
            <q-btn-dropdown
              flat
              class="user-dropdown q-pa-sm"
              color="primary"
              dropdown-icon="mdi-chevron-down"
              transition-show="scale"
              transition-hide="scale"
            >
              <template v-slot:label>
                <div class="row items-center no-wrap">
                  <span size="32px" color="primary" class="q-mr-sm">
                    <q-icon name="mdi-account" color="secondary" class="text-secondary" size="sm" />
                  </span>
                  <div class="text-weight-bold text-info">{{ firstName }} {{ lastName }}</div>
                </div>
              </template>

              <q-list class="modern-menu rounded-borders" >

                <q-item v-if="isAdmin" clickable @click="router.push('/adminDashboard')" v-ripple class="menu-item">
                  <q-item-section avatar>
                    <q-icon name="dashboard" color="primary" />
                  </q-item-section>
                  <q-item-section>داشبورد ادمین</q-item-section>
                </q-item>

                <q-item clickable v-ripple class="menu-item" :active="$route.path === '/wallet'" @click="navigateToWallet">
                  <q-item-section avatar>
                    <q-icon name="attach_money" color="secondary" />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>میزان دارایی</q-item-label>
                    <q-item-label caption>
                      {{ walletStore.goldAmount.toLocaleString() }} <span class="text-weight-bold">گرم</span>
                    </q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-badge color="positive" v-if="walletStore.goldAmount > 1000">
                      <q-icon name="trending_up" size="xs" />
                    </q-badge>
                  </q-item-section>
                </q-item>

                <q-separator />

                <q-item clickable v-ripple @click="handleLogout" class="menu-item">
                  <q-item-section avatar>
                    <q-icon name="logout" color="negative" />
                  </q-item-section>
                  <q-item-section>خروج</q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
        </div>
      </header>

      <!--  Content Container -->
      <div class="content-container">
        <div class="row q-col-gutter-lg">
          <!-- Enhanced Sidebar -->
          <sideBarDashboard />
          <div class="col-12 col-md-9">
            <q-page-container>
              <router-view
                class="routerPage"
                style="border-radius: 16px; background-color: transparent"
              />
            </q-page-container>
          </div>
        </div>
      </div>
    </div>
    <footerDashboard />
   <SupportBtn />
  </q-layout>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, computed, defineAsyncComponent,onMounted } from "vue";
import { useWalletStore } from "src/stores/wallet";
import { api } from "src/boot/axios";
import favicon from 'src/assets/faviicon.png'

const drawerDashboard = defineAsyncComponent(() => import('src/components/dashboard/sideBar/drawerDashboard.vue'))
const sideBarDashboard = defineAsyncComponent(() => import('src/components/dashboard/sideBar/sideBarDashboard.vue'))
const footerDashboard = defineAsyncComponent(() => import('src/components/dashboard/footerDashboard.vue'))

import { useAuthStore } from "src/stores/auth";
import SupportBtn from "src/components/supportBtn.vue";
const walletStore = useWalletStore()
const isAdmin = ref('')

const fetchUserInfo = async () => {
  try {
    await authStore.checkAuth();
    if (authStore.isAuthenticated) {
      const { data } = await api.get("/get-user-info");
      authStore.updateUserInfo(data.user_info);
      walletStore.setBalance(data.user_info.rial_balance)
      walletStore.setGoldAmount(data.user_info.gold_balance)
      localStorage.setItem('userId', data.user_info.id)
      if(data.user_info.user_type === 2){
        isAdmin.value = true
      }
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
};
onMounted(fetchUserInfo);

const router = useRouter();
const rightDrawerOpen = ref(false);

const authStore = useAuthStore();
const firstName = computed(() => authStore.firstName);
const lastName = computed(() => authStore.lastName);

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}






</script>

<style scoped>
.routerPage {
  border-radius: 16px;
  background-color: transparent;
  padding: 8px;
  border: 1px solid var(--q-info);
  margin: 0 5px;
  margin-bottom: 100px;
}
.background-pattern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 100vh;
  background: linear-gradient(180deg, var(--q-primary) 0%, var(--q-info) 50%);
  z-index: 0;
}

.gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100vh;
  background: linear-gradient(180deg, transparent 0%, transparent 30%, #f8fafc 100%);
}

.dashboard-page {
  background: #f8fafc;
  min-height: 100vh;
  direction: rtl;
}
.content-container {
  background-color: transparent;
}


.animated-waves {
  position: absolute;
  width: 100%;
  height: 100%;
  background-size: 60px 60px;
  animation: waveAnimation 10s linear infinite;
}

@keyframes waveAnimation {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 60px 60px;
  }
}

.gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(180deg, transparent 0%, #f8fafc 100%);
}

.main-container {
  max-width: 1440px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.header-section {
  padding-bottom: 80px;
  margin-bottom: -40px;
}

.text-glow {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  z-index: 2;
}


.modern-menu {
  border-radius: 12px;
  border: 1px solid var(--q-info);
}
.modern-menu1 {
  border-radius: 12px;
}

/* Enhanced Stats Cards */
.stats-card {
  height: 100%;
}

.rotating-icon {
  transition: transform 0.3s ease;
}

.stats-card:hover .rotating-icon {
  transform: rotate(15deg);
}

/* Enhanced Price Display */
.price-display {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(var(--q-primary), 0.2);
}

.price-display:hover {
  border-color: var(--q-primary);
  box-shadow: 0 4px 15px rgba(var(--q-primary), 0.15);
}

/* Shimmer Effect */
.shimmer {
  position: relative;
  overflow: hidden;
}

.shimmer::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 200%;
  }
}

/* Enhanced Buttons */
.trade-btn {
  border-radius: 12px;
  height: 56px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.trade-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--q-primary), 0.25);
}

.download-btn {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.download-btn:hover {
  transform: scale(1.02);
}

.buy-btn {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.buy-btn:hover {
  background: var(--q-primary);
  color: white;
}

/* Enhanced Feature Cards */
.feature-card {
  height: 100%;
}

.feature-icon {
  transition: all 0.4s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(10deg);
}

/* Notification Badge */
.notification-btn {
  position: relative;
}

.q-badge {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

/* Premium Badge */
.premium-badge {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 8px;
  border-radius: 12px;
  backdrop-filter: blur(5px);
}

/* User Dropdown */
.user-dropdown {
  border-radius: 12px;
  padding: 4px 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
}

.user-dropdown:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Pulse Icon */
.pulse-icon {
  animation: pulse-opacity 1.5s infinite;
}

@keyframes pulse-opacity {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}


/* Responsive Adjustments */
@media (max-width: 1023px) {
  .sticky-sidebar {
    position: relative;
    top: 0;
    margin-bottom: 24px;
  }

  .header-section {
    margin-bottom: -20px;
    padding-bottom: 60px;
  }

  .main-container {
    padding: 0 16px;
  }
  .sideBar {
    display: none;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(241, 245, 249, 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Accessibility Focus States */
.q-btn:focus,
.menu-item:focus {
  outline: 2px solid var(--q-primary);
  outline-offset: 2px;
}

/* Loading States */
.q-btn.loading {
  opacity: 0.8;
  pointer-events: none;
}
.user-dropdown {
  border-radius: 8px;
  transition: all 0.3s ease;
}
.user-dropdown:hover {
  background: rgba(0, 0, 0, 0.05);
}
.modern-menu {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.menu-item {
  border-radius: 4px;
  transition: background-color 0.2s ease;
}
.menu-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}
</style>
