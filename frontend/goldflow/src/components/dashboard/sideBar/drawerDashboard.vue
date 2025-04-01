<template>
  <q-drawer
              side="left"
              v-model="rightDrawerOpen"
              bordered
              :width="280"
            >
              <q-scroll-area class="fit">
                <div class="user-card q-pa-md rounded-borders bg-white">
                  <div class="row items-center no-wrap q-mb-sm">
                    <q-avatar color="primary" text-color="white" class="q-mr-sm">
                      <q-icon name="mdi-account-circle-outline" />
                    </q-avatar>
                    <div class="text-weight-bold text-h6 text-primary">{{ name }}</div>
                  </div>

                  <div class="row items-center q-mt-md">
                    <q-icon name="mdi-gold" color="secondary" size="sm" class="q-mr-xs" />
                    <span class="text-subtitle1">میزان دارایی:</span>
                    <span class="text-weight-medium text-secondary q-ml-sm">{{ goldAmount }}</span>
                  </div>
                </div>

                <q-separator class="q-my-md" />

                <!-- Mobile Auth Buttons -->
                <q-item
                  clickable
                  @click="router.push('/dashboard')"
                  v-ripple
                  class="menu-item rounded-borders"
                >
                  <q-item-section avatar>
                    <q-icon name="dashboard" color="secondary" />
                  </q-item-section>
                  <q-item-section class="text-h6">داشبورد </q-item-section>
                </q-item>
                <q-list padding class="modern-menu">
                  <q-item
                    clickable
                    @click="router.push('/dashboard/wallet')"
                    v-ripple
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="shopping_cart" color="primary" />
                    </q-item-section>
                    <q-item-section>خرید و فروش</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/dashboard/card')"
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="wallet" color="primary" />
                    </q-item-section>
                    <q-item-section> مدیریت کارت ها</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    v-ripple
                    class="menu-item rounded-borders"
                    @click="router.push('/dashboard/irt')"
                  >
                    <q-item-section avatar>
                      <q-icon name="account_balance_wallet" color="primary" />
                    </q-item-section>
                    <q-item-section>کیف پول</q-item-section>
                  </q-item>

                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/dashboard/reciept')"
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="history" color="primary" />
                    </q-item-section>
                    <q-item-section>تاریخچه معاملات</q-item-section>
                  </q-item>
                  <q-item
                    clickable
                    v-ripple
                    @click="router.push('/adminDashboard')"
                    class="menu-item rounded-borders"
                    v-if="isValid"
                  >
                    <q-item-section avatar>
                      <q-icon name="history" color="primary" />
                    </q-item-section>
                    <q-item-section>داشبورد ادمین </q-item-section>
                  </q-item>
                  <q-item
                    clickable
                    @click="handleLogout"
                    v-ripple
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon name="logout" color="negative" />
                    </q-item-section>
                    <q-item-section> خروج </q-item-section>
                  </q-item>
                </q-list>
              </q-scroll-area>
            </q-drawer>
</template>

<script setup>
import { computed, ref,watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { useWalletStore } from 'src/stores/wallet';

const router = useRouter()
const authStore = useAuthStore()
const walletStore = useWalletStore()
const name = computed(() => authStore.firstName);
const goldAmount = computed(() => walletStore.goldAmount)

const isValid = ref(!!localStorage.getItem('idType'));

watch(() => localStorage.getItem('idType'), (newValue) => {
  isValid.value = !!newValue;
});

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}

</script>

<style scoped>
.menu-item {
  border-radius: 8px;
  border: none;
  transition: all 0.2s ease;
}

.menu-item:hover {
  background: rgba(var(--q-primary), 0.1);
}
</style>
