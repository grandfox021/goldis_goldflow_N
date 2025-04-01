<template>
  <div class="q-pa-md">
    <!-- Amount Options -->
    <div class="option-grid">
      <q-card
        v-for="(option, index) in purchaseOptions"
        :key="index"
        :class="['option-card', { 'selected': selectedOption === option }]"
        @click="selectOption(option)"
      >
        <q-card-section class="q-py-md text-center">
          <div class="text-h6 text-weight-bold text-secondary">{{ option.amount }}
            <span class="text-subtitle1 text-accent">سوت</span>
          </div>

          <q-badge color="white" class="price-badge text-subtitle1 q-mt-sm q-pa-sm text-primary">
            {{ formatPrice(option.price) }}
            <span class="q-pl-xs text-accent">تومان</span>
          </q-badge>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useWalletStore } from 'src/stores/wallet';
import { useRouter } from 'vue-router';

const selectedOption = ref(null);
const customAmount = ref(null);
const walletStore = useWalletStore();
const currentPrice = computed(() => walletStore.price);
const router = useRouter();

const purchaseOptions = computed(() => [
  {
    amount: 100,
    price: calculatePrice(100)
  },
  {
    amount: 300,
    price: calculatePrice(300)
  },
  {
    amount: 500,
    price: calculatePrice(500)
  }
]);

function calculatePrice(amount) {
  return (amount * currentPrice.value / 1000).toFixed(0);
}

// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};

const selectOption = (option) => {
  selectedOption.value = option;
  customAmount.value = null;
  sendData();
};

const sendData = () => {
  router.push({path: '/dashboard/wallet', query: {data: selectedOption.value.amount}});
  console.log(selectedOption.value);
};
</script>

<style scoped>
.option-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .option-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 479px) {
  .option-grid {
    grid-template-columns: 1fr;
  }
}

.option-card {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.option-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.option-card.selected {
  border-color: var(--q-primary);
  background-color: rgba(var(--q-primary-rgb), 0.05);
}

.price-badge {
  border-radius: 8px;
  display: inline-block;
  width: auto;
}

/* Ensure text remains readable at all sizes */
@media (max-width: 320px) {
  .text-h6 {
    font-size: 1rem;
  }

  .text-subtitle1 {
    font-size: 0.875rem;
  }

  .q-card-section {
    padding: 8px !important;
  }
}
</style>
