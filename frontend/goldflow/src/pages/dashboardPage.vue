<template>
  <q-page class="dashboard-page">
    <div class="main-container bg-white">
      <!-- Enhanced Content Container with better mobile spacing -->
      <div class="content-container q-px-md q-px-lg-lg">
        <div class="row q-col-gutter-md q-col-gutter-lg-lg">
          <!-- Main Content Area with improved responsiveness -->
          <div class="col-12">
            <!-- Stats Cards with improved mobile layout -->
            <div dir="rtl" class="row reveal-section q-col-gutter-md">
              <div class="col-12 col-sm-6 col-md-4">
                <div class="stat-card">
                  <div class="stat-icon">
                    <q-icon name="timeline" size="32px" />
                  </div>
                  <div class="stat-content">
                    <div class="stat-label">قیمت لحظه‌ای طلا</div>
                    <div class="stat-value value-animate">
                      {{ formatPrice(currentPrice) }}
                      <span class="text-caption q-ml-xs">تومان</span>
                    </div>
                    <div class="stat-change positive">
                      <q-icon name="trending_up" size="16px" />
                      ۲.۵٪ <span class="period">۲۴ ساعت گذشته</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12 col-sm-6 col-md-4">
                <div class="stat-card">
                  <div class="stat-icon secondary">
                    <q-icon name="account_balance" size="32px" />
                  </div>
                  <div class="stat-content">
                    <div class="stat-label">موجودی خزانه</div>
                    <div class="stat-value value-animate" v-persian-input>
                      {{ treasuryBalance }}
                      <span class="text-caption q-ml-xs">گرم</span>
                    </div>
                    <div class="stat-update">
                      <q-icon name="update" size="16px" class="rotate-icon" />
                      بروزرسانی: ۵ دقیقه پیش
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12 col-sm-6 col-md-4">
                <div class="stat-card">
                  <div class="stat-icon accent">
                    <q-icon color="secondary" name="account_balance_wallet" size="32px" />
                  </div>
                  <div class="stat-content">
                    <div class="stat-label">کیف پول شما</div>
                    <div class="stat-value value-animate flex flex-center">
                      {{ formatPrice(balance) }}
                      <span class="text-caption q-ml-xs">تومان</span>
                    </div>
                    <q-btn
                      flat
                      dense
                      color="primary"
                      class="wallet-btn q-px-sm"
                      icon="add_circle_outline"
                      @click="router.push('/dashboard/deposite')"
                      label="شارژ کیف پول"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Enhanced Quick Trade Section with better mobile layout -->
            <q-card dir="rtl" class="trade-card modern-card q-mt-md q-mt-lg-lg reveal-section">
              <q-card-section>
                <div class="row items-center justify-between q-mb-md">
                  <div class="text-h6 text-weight-bold flex items-center">
                    <q-icon
                      name="swap_horiz"
                      size="26px"
                      class="q-mr-sm text-primary floating-icon"
                    />
                    معامله سریع
                  </div>
                </div>

                <div class="row q-col-gutter-md">
                  <div class="col-12 col-md-8">
                    <q-card
                      flat
                      bordered
                      class="price-display q-pa-md q-pa-lg-lg modern-card"
                    >
                      <div class="text-h6 text-lg text-weight-bold">
                        قیمت هر گرم:
                        <span class="text-primary text-weight-bold price-highlight shimmer"
                          >{{ formatPrice(currentPrice) }}</span
                        >
                        <span class="text-caption q-ml-sm">تومان</span>
                      </div>
                      <div class="row items-center q-mt-sm">
                        <q-icon
                          name="schedule"
                          size="16px"
                          class="q-mr-xs text-grey-7 pulse-icon"
                        />
                        <div class="text-caption text-grey-7">
                          بروزرسانی: <span class="syncing-text">۱۰ ثانیه پیش</span>
                        </div>
                      </div>
                    </q-card>
                  </div>
                  <div class="col-12 col-md-4">
                    <q-btn
                      unelevated
                      class="full-width trade-btn text-accent"
                      color="primary"
                      label="خرید جدید"
                      icon-right="add"
                      @click="router.push('/dashboard/wallet')"
                    />
                  </div>
                </div>
                <FastBuyComponent />
              </q-card-section>
            </q-card>

            <!-- Enhanced Features Section with better mobile layout -->
            <div class="row q-col-gutter-md q-mt-md q-mt-lg-lg q-pb-xl reveal-section">
              <div class="col-12 col-sm-6 col-md-4">
                <q-card class="feature-card modern-card">
                  <q-card-section class="text-center">
                    <div class="icon-container">
                      <q-icon
                        name="security"
                        size="52px"
                        class="text-primary q-mb-sm q-mb-md-md feature-icon"
                      />
                    </div>
                    <div class="text-subtitle1 text-h6-md text-weight-medium">امنیت سرمایه</div>
                    <div class="text-body2 q-mt-sm q-mt-md-md text-grey-7">
                      با بیمه کامل و ضمانت اصالت
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-sm-6 col-md-4">
                <q-card class="feature-card modern-card">
                  <q-card-section class="text-center">
                    <div class="icon-container">
                      <q-icon
                        name="payments"
                        size="52px"
                        class="text-primary q-mb-sm q-mb-md-md feature-icon"
                      />
                    </div>
                    <div class="text-subtitle1 text-h6-md text-weight-medium">تضمین نقدشوندگی</div>
                    <div class="text-body2 q-mt-sm q-mt-md-md text-grey-7">
                      واریز وجه در کمتر از ۴ ساعت
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-sm-6 col-md-4 col-sm-offset-3 col-md-offset-0">
                <q-card class="feature-card modern-card">
                  <q-card-section class="text-center">
                    <div class="icon-container">
                      <q-icon
                        name="support_agent"
                        size="52px"
                        class="text-primary q-mb-sm q-mb-md-md feature-icon"
                      />
                    </div>
                    <div class="text-subtitle1 text-h6-md text-weight-medium">پشتیبانی ۲۴/۷</div>
                    <div class="text-body2 q-mt-sm q-mt-md-md text-grey-7">
                      همراه شما در تمام لحظات
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </div>
        </div>
      </div>

      
    </div>
  </q-page>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useWalletStore } from "src/stores/wallet";
import { useRouter } from "vue-router";
import FastBuyComponent from "src/components/dashboard/fastBuyComponent.vue";
const router = useRouter();
const useWallet = useWalletStore();
const currentPrice = computed(() => useWallet.price);
const treasuryBalance = ref("2638.79");
const balance = computed(() => (useWallet.balance / 10).toFixed(0));



// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};

// Add reveal animation on component mount with improved reveal timing
onMounted(() => {
  const sections = document.querySelectorAll('.reveal-section');

  // Enhanced intersection observer with staggered animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        // Add staggered delay based on index
        setTimeout(() => {
          entry.target.classList.add('revealed');
        }, index * 150);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  sections.forEach(section => {
    observer.observe(section);
  });

  // Initialize price update simulation
  initPriceUpdateSimulation();
});

// Simulate price updates for better UX demo
const initPriceUpdateSimulation = () => {
  const priceElements = document.querySelectorAll('.syncing-text');

  setInterval(() => {
    priceElements.forEach(el => {
      el.textContent = '۵ ثانیه پیش';

      setTimeout(() => {
        el.textContent = '۱۰ ثانیه پیش';
      }, 5000);
    });
  }, 10000);
};
</script>

<style scoped>
.dashboard-page {
  background: #f8fafc;
  min-height: 100vh;
  direction: rtl;
}

.main-container {
  max-width: 1440px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  padding-top: 1rem;
  border-radius: 12px;
}

.modern-card {
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.03);
  overflow: hidden;
}

.modern-card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 6px 20px rgba(0, 0, 0, 0.08),
    0 2px 6px rgba(0, 0, 0, 0.04);
}

/* Enhanced Stats Cards with Better Mobile Adaptation */
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 0.875rem;
  border-left: 3px solid var(--q-primary);
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  box-shadow:
    0 4px 10px -2px rgba(0, 0, 0, 0.06),
    0 2px 4px -1px rgba(0, 0, 0, 0.02);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow:
    0 8px 20px -5px rgba(0, 0, 0, 0.08),
    0 4px 8px -4px rgba(0, 0, 0, 0.03);
  border-color: rgba(200, 220, 240, 0.6);
}

.stat-icon {
  background: rgba(var(--q-primary-rgb), 0.12);
  color: var(--q-secondary);
  padding: 1rem;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 4px 8px -2px rgba(var(--q-primary-rgb), 0.15);
}

.stat-card:hover .stat-icon {
  transform: scale(1.05) rotate(3deg);
  background: rgba(var(--q-primary-rgb), 0.15);
  box-shadow: 0 5px 10px -2px rgba(var(--q-primary-rgb), 0.2);
}

.stat-icon.secondary {
  background: rgba(var(--q-secondary-rgb), 0.12);
  color: var(--q-secondary);
  box-shadow: 0 4px 8px -2px rgba(var(--q-secondary-rgb), 0.15);
}

.stat-card:hover .stat-icon.secondary {
  background: rgba(var(--q-secondary-rgb), 0.15);
  box-shadow: 0 5px 10px -2px rgba(var(--q-secondary-rgb), 0.2);
}

.stat-icon.accent {
  background: rgba(var(--q-accent-rgb), 0.12);
  color: var(--q-accent);
  box-shadow: 0 4px 8px -2px rgba(var(--q-accent-rgb), 0.15);
}

.stat-card:hover .stat-icon.accent {
  background: rgba(var(--q-accent-rgb), 0.15);
  box-shadow: 0 5px 10px -2px rgba(var(--q-accent-rgb), 0.2);
}

.stat-content {
  flex: 1;
}

.stat-label {
  color: #64748b;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}

.value-animate {
  transition: all 0.3s ease;
}

.value-animate:hover {
  color: var(--q-primary);
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  font-weight: 500;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change .period {
  color: #64748b;
  margin-right: 0.4rem;
  font-weight: normal;
  font-size: 0.75rem;
}

.stat-update {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  color: #64748b;
}

.rotate-icon {
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Enhanced Trade Card with Better Mobile UX */
.trade-card {
  border-left: 3px solid var(--q-primary);
}

.price-display {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(var(--q-primary-rgb), 0.2);
  transition: all 0.3s ease;
}

.price-display:hover {
  border-color: var(--q-primary);
  box-shadow: 0 6px 16px -4px rgba(var(--q-primary-rgb), 0.2);
}

.price-highlight {
  font-size: 1.6rem;
  position: relative;
  padding: 0 0.4rem;
  border-radius: 4px;
}

/* Enhanced Shimmer Effect */
.shimmer {
  position: relative;
  overflow: hidden;
}

.shimmer::after {
  content: "";
  position: absolute;
  top: 0;
  left: -150%;
  width: 80%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.5),
    transparent
  );
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% {
    left: -150%;
  }
  100% {
    left: 200%;
  }
}

/* Syncing Text Animation */
.syncing-text {
  position: relative;
}

.syncing-text::after {
  content: "";
  position: absolute;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background-color: #10b981;
  right: -10px;
  top: 50%;
  transform: translateY(-50%);
  animation: blink 2s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* Enhanced Buttons with Mobile-Friendly Touch Areas */
.trade-btn {
  border-radius: 8px;
  height: 54px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 5px 14px -2px rgba(var(--q-primary-rgb), 0.25);
}

.trade-btn:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 10px 22px -4px rgba(var(--q-primary-rgb), 0.35);
}

.wallet-btn {
  border-radius: 6px;
  transition: all 0.3s ease;
  font-weight: 500;
  padding: 3px 10px;
}

.wallet-btn:hover {
  background: rgba(var(--q-primary-rgb), 0.1);
  transform: translateY(-2px);
}

/* Enhanced Feature Cards with Better Mobile Layout */
.feature-card {
  height: 100%;
  padding: 0.5rem;
  border: 1px solid rgba(235, 240, 245, 0.8);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.feature-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 12px 25px -8px rgba(0, 0, 0, 0.12);
  border-color: rgba(200, 220, 240, 0.6);
}

.icon-container {
  position: relative;
  display: inline-block;
  margin-bottom: 0.75rem;
}

.icon-container::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: radial-gradient(circle, rgba(var(--q-primary-rgb), 0.1) 0%, transparent 70%);
  border-radius: 50%;
  z-index: -1;
  transform: scale(0.8);
  opacity: 0;
  transition: all 0.4s ease;
}

.feature-card:hover .icon-container::after {
  transform: scale(1.4);
  opacity: 1;
}

.feature-icon {
  filter: drop-shadow(0 4px 5px rgba(var(--q-primary-rgb), 0.25));
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.feature-card:hover .feature-icon {
  transform: scale(1.08) rotate(4deg);
  filter: drop-shadow(0 6px 12px rgba(var(--q-primary-rgb), 0.3));
}

/* Floating Icon Animation */
.floating-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* Pulse Icon */
.pulse-icon {
  animation: pulse-opacity 1.5s infinite;
}

@keyframes pulse-opacity {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

/* Reveal Animation for Sections - Improved for mobile */
.reveal-section {
  opacity: 0;
  transform: translateY(16px);
  transition: all 0.7s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.reveal-section.revealed {
  opacity: 1;
  transform: translateY(0);
}

/* New Mobile Quick Actions Menu */
.mobile-quick-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  z-index: 10;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);
  display: none;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}

.action-btn {
  padding: 8px 0;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.action-btn:active {
  background: rgba(var(--q-primary-rgb), 0.1);
}

/* Responsive Adjustments with Mobile-First Approach */
@media (max-width: 599px) {
  .main-container {
    padding: 0.5rem 0.5rem 70px 0.5rem; /* Added bottom padding for mobile actions */
  }

  .mobile-quick-actions {
    display: block;
  }

  .stat-card {
    padding: 0.75rem;
  }

  .stat-icon {
    padding: 0.75rem;
  }

  .stat-value {
    font-size: 1.2rem;
  }

  .price-highlight {
    font-size: 1.3rem;
  }

  .trade-btn {
    height: 48px;
  }

  /* Stack feature cards nicely */
  .feature-card {
    margin-bottom: 0.75rem;
  }

  /* Optimize touch targets for mobile */
  .q-btn {
    min-height: 40px;
  }

  /* Better typography for small screens */
  .text-h6 {
    font-size: 1.1rem;
  }
}

@media (min-width: 600px) and (max-width: 1023px) {
  .main-container {
    padding: 0.75rem 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-value {
    font-size: 1.3rem;
  }

  /* Better spacing for tablets */
  .q-col-gutter-md {
    margin: -8px;
  }

  .q-col-gutter-md > * {
    padding: 8px;
  }
}

/* Conditional Mobile Classes */
@media (min-width: 1024px) {
  .q-px-lg-lg {
    padding-left: 24px;
    padding-right: 24px;
  }

  .q-mt-lg-lg {
    margin-top: 24px;
  }

  .q-pa-lg-lg {
    padding: 24px;
  }

  .q-col-gutter-lg-lg {
    margin: -12px;
  }

  .q-col-gutter-lg-lg > * {
    padding: 12px;
  }

  .q-mb-md-md {
    margin-bottom: 16px;
  }

  .q-mt-md-md {
    margin-top: 16px;
  }

  .text-h6-md {
    font-size: 1.25rem;
  }
}

/* Custom Scrollbar - More subtle and mobile friendly */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(241, 245, 249, 0.5);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
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
</style>
