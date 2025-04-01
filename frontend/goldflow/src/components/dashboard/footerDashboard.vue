<template>
  <!-- Mobile Quick Actions - New Component -->
  <div dir="rtl" class="mobile-quick-actions q-pa-md reveal-section q-mt-md">
        <div class="row q-col-gutter-sm">
          <div class="col-4">
            <q-btn flat color="primary" class="full-width action-btn" @click="router.push('/dashboard/irt')">
              <div class="column items-center">
                <q-icon name="account_balance_wallet" size="24px" />
                <div class="text-caption q-mt-xs">کیف پول</div>
              </div>
            </q-btn>
          </div>
          <div class="col-4">
            <q-btn flat color="primary" class="full-width action-btn" @click="router.push('/dashboard/wallet')">
              <div class="column items-center">
                <q-icon name="shopping_cart" size="24px" />
                <div class="text-caption q-mt-xs">خرید</div>
              </div>
            </q-btn>
          </div>
          <div class="col-4">
            <q-btn flat color="primary" class="full-width action-btn" @click="router.push('/dashboard/support')">
              <div class="column items-center">
                <q-icon name="headset_mic" size="24px" />
                <div class="text-caption q-mt-xs">پشتیبانی</div>
              </div>
            </q-btn>
          </div>
        </div>
      </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()
</script>

<style scoped>
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
