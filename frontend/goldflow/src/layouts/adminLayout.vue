<template>
  <q-layout view="lHh Lpr lFf">
    <div class="main-container">
      <!-- Enhanced Gradient Background -->
      <div class="background-pattern">
        <div class="animated-waves"></div>
        <div class="gradient-overlay"></div>
      </div>
      <!--  Header -->
      <header class="header-section q-px-lg q-pt-md">
        <div class="row justify-between items-center q-pb-xl">
          <!-- Hamburger menu for mobile -->
          <div class="lt-md">
            <q-btn
              icon="menu"
              flat
              color="info"
              class="lt-md"
              @click="rightDrawerOpen = !rightDrawerOpen"
              aria-label="Menu"
            />
            <q-drawer
              side="left"
              v-model="rightDrawerOpen"
              bordered
              class="mobile-drawer"
              :width="280"
            >
              <q-scroll-area class="fit">
                <div class="text-accet q-pa-sm">
                  <div class="text-weight-bold">
                    <q-icon
                      size="sm"
                      color="primary"
                      name="mdi-shield-account"
                    />
                    پنل مدیریت
                  </div>
                  <div>
                    ادمین: {{ adminName }}
                  </div>
                </div>

                <q-separator class="q-my-md" />

                <!-- Mobile Admin Menu -->
                <q-item
                  clickable
                  @click="router.push('/adminDashboard')"
                  v-ripple
                  class="menu-item rounded-borders"
                >
                  <q-item-section avatar>
                    <q-icon name="dashboard" color="secondary" />
                  </q-item-section>
                  <q-item-section class="text-h6">داشبورد مدیریت</q-item-section>
                </q-item>

                <q-list padding class="modern-menu">
                  <q-item
                    clickable
                    @click="router.push('/adminDashboard/tickets')"
                    v-ripple
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="people" color="primary" />
                    </q-item-section>
                    <q-item-section>مدیریت تیکت ها</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/adminDashboard/orders')"
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="shopping_cart" color="primary" />
                    </q-item-section>
                    <q-item-section>معاملات</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/adminDashboard/settings')"
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="settings" color="primary" />
                    </q-item-section>
                    <q-item-section>تنظیمات</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    @click="logout"
                    v-ripple
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="logout" color="negative" />
                    </q-item-section>
                    <q-item-section>خروج</q-item-section>
                  </q-item>
                </q-list>
              </q-scroll-area>
            </q-drawer>
          </div>

          <!-- Admin Logo -->
          <div class="text-h4 flex flex-center items-center">
            <q-avatar size="48px" class="q-mr-md shadow-2">
              <img :src="favicon" alt="logo" />
            </q-avatar>
            <span class="text-weight-medium text-info q-pa-sm text-glow"
              >گلدیس <small class="text-body1">پنل مدیریت</small></span
            >
          </div>

          <!-- Enhanced Admin Menu -->
          <div class="row items-center q-gutter-x-md gt-sm">
            <q-btn-dropdown
              flat
              class="user-dropdown glossy q-pa-md"
              color="info"
              dropdown-icon="mdi-chevron-down"
            >
              <template v-slot:label>
                <div class="row items-center q-pa-xs no-wrap">
                  <q-icon name="admin_panel_settings" size="sm" class="q-mr-xs" />
                  <div class="text-white">
                    <div class="text-weight-bold text-secondary">{{ adminName }}</div>
                  </div>
                </div>
              </template>

              <q-list class="modern-menu">
                <q-item clickable @click="router.push('/dashboard')" v-ripple class="q-pr-xs">
                  <q-item-section avatar>
                    <q-icon name="home" color="primary" />
                  </q-item-section>
                  <q-item-section class="q-pr-xl">داشبورد کاربری</q-item-section>
                </q-item>
                <q-item clickable v-ripple class="q-pr-xs">
                  <q-item-section avatar>
                    <q-icon name="settings" color="grey-7" />
                  </q-item-section>
                  <q-item-section>تنظیمات</q-item-section>
                </q-item>
                <q-item
                  clickable
                  v-ripple
                  @click="logout"
                  class="q-pr-xs"
                >
                  <q-item-section avatar>
                    <q-icon name="logout" color="negative" />
                  </q-item-section>
                  <q-item-section>خروج</q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>

            <!-- Notification Badge -->
            <q-btn round flat color="secondary" class="notification-btn q-pr-sm">
              <q-icon name="notifications" />
              <q-badge color="red" floating>3</q-badge>
            </q-btn>
          </div>
        </div>
      </header>

      <!--  Content Container -->
      <div class="content-container q-px-lg">
        <div class="row q-col-gutter-lg">
          <!-- Enhanced Admin Sidebar -->
          <div class="col-12 col-md-3 sideBar">
            <div class="q-pa-sm bordeDiv col-12 col-md-3">
              <q-card class="sticky-sidebar bg-white modern-card q-pa-md">
                <q-item
                  clickable
                  @click="router.push('/adminDashboard')"
                  v-ripple
                  class="menu-item rounded-borders"
                >
                  <q-item-section avatar>
                    <q-icon name="admin_panel_settings" color="secondary" />
                  </q-item-section>
                  <q-item-section class="text-h6">داشبورد مدیریت</q-item-section>
                </q-item>

                <q-separator />

                <q-list padding class="modern-menu1">
                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/adminDashboard/tickets')"
                    >
                    <q-item-section avatar>
                      <q-icon name="mdi-ticket-confirmation" color="primary" />
                    </q-item-section>
                    <q-item-section>مدیریت تیکت ها</q-item-section>
                  </q-item>
                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/adminDashboard/orders')"
                    >
                    <q-item-section avatar>
                      <q-icon name="shopping_cart" color="primary" />
                    </q-item-section>
                    <q-item-section> مدیریت معاملات</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    @click="router.push('/adminDashboard/settings')"
                    v-ripple
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="settings" color="primary" />
                    </q-item-section>
                    <q-item-section>تنظیمات</q-item-section>
                  </q-item>
                </q-list>
              </q-card>
            </div>
          </div>

          <!-- Main Content Area -->
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
  </q-layout>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, computed } from "vue";
import { useAuthStore } from "src/stores/auth";

import favicon from 'src/assets/faviicon.png'

const router = useRouter();
const rightDrawerOpen = ref(false);
const authStore = useAuthStore();
const adminName = computed(() => authStore.firstName || "مدیر سیستم");



// Logout function
const logout = () => {
  authStore.logout()
  router.push('/')
};
</script>

<style scoped>
.routerPage {
  border-radius: 16px;
  background-color: transparent;
  padding: 8px;
  border: 1px solid var(--q-info);
  margin: 0 5px;
}

.dashboard-page {
  background: #f8fafc;
  min-height: 100vh;
  direction: rtl;
}
.content-container {
  background-color: transparent;
}

.sideBar {
  position: relative;
}
.bordeDiv {
  border: 1px solid var(--q-info);
  position: absolute;
  z-index: 5;
  width: 100%;
  border-radius: 16px;
}

.background-pattern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 300px;
  background: linear-gradient(180deg, var(--q-primary) 50%, var(--q-info)100%);
  z-index: 0;
  overflow: hidden;
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

/* Modern Card Styling */
.modern-card {
  border-radius: 16px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  background-color: transparent;
}

.modern-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
}

/* Enhanced Sidebar */
.sticky-sidebar {
  position: sticky;
  top: 20px;
  background: transparent;
}

.modern-menu {
  border-radius: 12px;
  border: 1px solid var(--q-info);
}
.modern-menu1 {
  border-radius: 12px;
}

.menu-item {
  border-radius: 8px;
  border: none;
  transition: all 0.2s ease;
}

.menu-item:hover {
  background: rgba(var(--q-primary), 0.1);
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

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
  .dashboard-page {
    background: #0f172a;
  }

  .gradient-overlay {
    background: linear-gradient(180deg, transparent 0%, #0f172a 100%);
  }

  .modern-card {
    background: rgba(30, 41, 59, 0.95);
    border-color: rgba(255, 255, 255, 0.05);
  }

  .menu-item:hover {
    background: rgba(255, 255, 255, 0.05);
  }

  .price-display {
    background: rgba(30, 41, 59, 0.9);
  }

  .text-grey-7,
  .text-grey-8 {
    color: #94a3b8 !important;
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
</style>
