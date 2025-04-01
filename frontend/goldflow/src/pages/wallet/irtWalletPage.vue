<template>
  <q-page class="wallet-page q-py-md">
        <div class="wallet-card bg-white q-pa-lg">
          <!-- Header with Logo & Title -->
          <div class="wallet-header q-mb-md">
            <div class="flex flex-center">
              <div class="flex column items-center justify-center">
                <q-icon name="account_balance_wallet" size="32px" color="primary" class="pulse-on-load q-mr-sm" />
                <div class="text-h6 text-primary">کیف پول تومانی شما</div>
              </div>
            </div>
          </div>

          <q-separator class="q-mb-lg separator-gradient" />

          <!-- Balance Section (with enhanced animations) -->
          <div class="balance-container q-pa-lg q-mb-lg">
            <div class="row items-center justify-between">
              <div class="text-subtitle1 text-weight-medium">موجودی:</div>
              <div class="flex">
                <div class="flex column flex-center">
                  <transition name="fade" mode="out-in">
                  <div class="balance-value" v-if="showBalance" key="visible">
                    <span class="text-h6 gt-sm:text-h5 text-weight-bold text-primary">{{ formatPrice(balance) }} تومان</span>
                  </div>
                  <div class="balance-value" v-else key="hidden">
                    <span class="text-h4 text-weight-bold text-primary">• • • • • •</span>
                  </div>
                </transition>
                <transition name="fade" mode="out-in">
                  <div class="balance-value" v-if="showBalance" key="visible">
                    <span class="text-h5 text-weight-bold text-secondary">{{ goldAmount }} گرم</span>
                  </div>
                  <div class="balance-value" v-else key="hidden">
                    <span class="text-h4 text-weight-bold text-primary">• • • • • •</span>
                  </div>
                </transition>
                </div>
                <q-btn flat dense round class="q-ml-sm toggle-visibility-btn"
                  :color="showBalance ? 'primary' : 'grey'"
                  :icon="showBalance ? 'visibility_off' : 'visibility'"
                  @click="toggleBalance">
                  <q-tooltip>{{ showBalance ? 'پنهان کردن موجودی' : 'نمایش موجودی' }}</q-tooltip>
                </q-btn>
              </div>
            </div>

            <!-- Real-time update indicator (appears during transactions) -->
            <transition name="slide-fade">
              <div class="update-indicator q-mt-sm" v-if="showUpdateIndicator">
                <q-spinner-dots color="secondary" size="1em" class="q-mr-xs" />
                <span class="text-caption text-secondary">در حال به‌روزرسانی موجودی...</span>
              </div>
            </transition>
          </div>

          <!-- Action Buttons (Enhanced) -->
          <div class="row q-col-gutter-md q-mb-lg">
            <div class="col-6">
              <q-btn unelevated color="primary" class="full-width action-button deposit-btn"
                @click="router.push('/dashboard/deposite')">
                <div class="row items-center justify-center">
                  <q-icon name="add" size="24px" class="q-mr-sm" />
                  <span>واریز</span>
                </div>
                <q-tooltip>افزایش موجودی کیف پول</q-tooltip>
              </q-btn>
            </div>
            <div class="col-6">
              <q-btn unelevated color="secondary" class="full-width action-button withdraw-btn"
                @click="router.push('/dashboard/withdraw')">
                <div class="row items-center justify-center">
                  <q-icon name="remove" size="24px" class="q-mr-sm" />
                  <span>برداشت</span>
                </div>
                <q-tooltip>برداشت از کیف پول</q-tooltip>
              </q-btn>
            </div>
          </div>

          <!-- Features Grid (Card-based design) -->
          <div class="features-section q-mb-lg">
            <div class="text-subtitle1 text-left text-weight-medium q-mb-sm">امکانات ویژه:</div>
            <div class="row q-col-gutter-md">
              <div class="col-12 col-sm-6" v-for="(feature, index) in features" :key="index">
                <div class="feature-card q-pa-md">
                  <q-icon :name="feature.icon" size="28px" class="text-primary q-mb-sm feature-icon" />
                  <div class="text-body2">{{ feature.title }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>


        <TarakoneshComponent />

  </q-page>
</template>

<script setup>
import { ref,  onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useWalletStore } from "src/stores/wallet";
import TarakoneshComponent from "src/components/dashboard/tarakoneshComponent.vue";

// States
const walletStore = useWalletStore()
const showBalance = ref(true);
const showUpdateIndicator = ref(false);
const balance = computed(() => walletStore.balance / 10)
const goldAmount = computed(() => walletStore.goldAmount)
const router = useRouter()

// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};

// Feature cards data
const features = ref([
  {
    icon: "schedule",
    title: "امکان برداشت ۲۴ ساعته به حساب بانکی"
  },
  {
    icon: "autorenew",
    title: "واریز خودکار و آنی به حساب شما"
  },
  {
    icon: "payments",
    title: "امکان افزایش موجودی از طریق درگاه پرداخت"
  },
  {
    icon: "swap_horiz",
    title: "امکان تبدیل موجودی به طلا به صورت لحظه‌ای"
  }
]);



// Toggle balance visibility with animation
const toggleBalance = () => {
  showBalance.value = !showBalance.value;
};



// Lifecycle
onMounted(() => {
  walletStore.setGoldAmount()
  walletStore.setBalance()

});

</script>

<style scoped>


.glassmorphic {
  background: var(--glassmorphic-bg-light);
  backdrop-filter: blur(10px);
  border: var(--glassmorphic-border-light);
  box-shadow: var(--card-shadow-light);
}

.feature-card {
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.balance-container {
  border-radius: 16px;

}

.separator-gradient {
  background: linear-gradient(to right, transparent, rgba(0, 0, 0, 0.1), transparent);
}


.wallet-card-container {
  perspective: 1000px;
}

.wallet-card {
  border-radius: 16px;
}


.wallet-header {
  position: relative;
}

.gradient-text {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 700;
}

.balance-container {
  border-radius: 16px;
  transition: all 0.3s ease;
}

.balance-value {
  min-width: 200px;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.action-button {
  height: 54px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.action-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-100%);
}

.action-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.action-button:hover::after {
  transform: translateX(0);
  transition: transform 0.5s ease;
}

.deposit-btn {
  background: var(--primary-gradient);
}

.withdraw-btn {
  background: var(--secondary-gradient);
}

.feature-card {
  border-radius: 16px;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 16px;
}

.feature-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.2);
}

.transactions-preview {
  border-radius: 24px;
}

.transaction-item {
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.transaction-item:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.transaction-skeleton {
  height: 60px;
  border-radius: 8px;
}

.theme-toggle-btn {
  transition: all 0.3s ease;
  z-index: 1000;
}

.theme-toggle-btn:hover {
  transform: rotate(45deg);
}

.toggle-visibility-btn {
  transition: all 0.3s ease;
}

.toggle-visibility-btn:hover {
  animation: pulse 1s infinite;
}

.update-indicator {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

/* Animations */
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

.pulse-on-load {
  animation: pulse 1.5s ease-in-out;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}


/* Responsive adjustments */
@media (max-width: 599px) {
  .balance-value {
    min-width: 150px;
  }

  .wallet-card {
    padding: 16px !important;
  }

  .action-button {
    height: 48px;
    font-size: 0.9rem;
  }

  .balance-container {
    padding: 16px !important;
  }
}
</style>
