<template>
  <div class="col-12 col-md-3 sideBar">
            <div class="q-pa-sm bordeDiv col-12 col-md-3">
              <q-card class="sticky-sidebar bg-white modern-card q-pa-md">
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

                <q-separator />

                <q-list
                  v-for="item in items"
                  :key="item.id"
                  padding
                  class="modern-menu1"
                >
                  <q-expansion-item
                    v-if="item.children"
                    expand-separator
                    :content-inset-level="0.5"
                    @click="router.push(item.route)"
                  >
                    <template v-slot:header>
                      <q-item-section avatar>
                        <q-icon :name="item.icon" color="primary" />
                      </q-item-section>
                      <q-item-section>{{ item.name }}</q-item-section>
                    </template>

                    <q-item
                      v-for="k in item.children"
                      :key="k.id"
                      clickable
                      @click="router.push(k.route)"
                      class="flex flex-center"
                    >
                      <q-icon size="md" color="secondary"> -</q-icon>
                      <q-item-section>{{ k.name }}</q-item-section>
                    </q-item>
                  </q-expansion-item>

                  <q-item
                    v-else
                    clickable
                    @click="router.push(item.route)"
                    v-ripple
                    class="menu-item rounded-borders"
                  >
                    <q-item-section avatar>
                      <q-icon :name="item.icon" color="primary" />
                    </q-item-section>
                    <q-item-section>{{ item.name }}</q-item-section>
                  </q-item>
                </q-list>
              </q-card>
            </div>
          </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const items = ref([
  {
    id: 1,
    name: "خرید و فروش",
    icon: "shopping_cart",
    route: "/dashboard/wallet",
  },
  { id: 2, name: "مدیریت کارت ها", icon: "wallet", route: "/dashboard/card" },
  {
    id: 3,
    name: "کیف پول",
    icon: "account_balance_wallet",
    route: "/dashboard/irt",
    children: [
      {
        id: 31,
        name: "افزایش اعتبار",
        route: "/dashboard/deposite",
        icon: "money",
      },
      {
        id: 32,
        name: "برداشت وجه",
        route: "/dashboard/withdraw",
        icon: "money",
      },
    ],
  },
  {
    id: 4,
    name: "تاریخچه معاملات",
    icon: "history",
    route: "/dashboard/reciept",
  },
]);
</script>

<style scoped>
.sideBar {
  position: relative;
}
.sticky-sidebar {
  position: sticky;
  top: 20px;
  background: transparent;
}
.bordeDiv {
  border: 1px solid var(--q-info);
  position: absolute;
  z-index: 5;
  width: 100%;
  border-radius: 16px;
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


.modern-menu {
  border-radius: 12px;
  border: 1px solid var(--q-info);
}
.modern-menu1 {
  border-radius: 12px;
}

/* Responsive Adjustments */
@media (max-width: 1023px) {
  .sticky-sidebar {
    position: relative;
    top: 0;
    margin-bottom: 24px;
  }
  .sideBar {
    display: none;
  }
}
</style>
