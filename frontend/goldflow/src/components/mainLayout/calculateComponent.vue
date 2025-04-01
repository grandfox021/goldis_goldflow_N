<template>
  <q-page class="flex justify-center items-center q-mb-xl q-pt-lg">
    <q-card
      class="calculator-card q-pa-md q-pa-lg-xl"
      style="width: 100%; max-width: 800px"
    >
      <div class="row q-col-gutter-md">
        <!-- Header - Full Width -->
        <div class="col-12 text-center q-mb-md">
          <div class="text-h4 text-weight-bold gold-title">
            ماشین حساب خرید و فروش
          </div>
        </div>

        <!-- Left side - Gold Type Selection -->
        <div class="col-12 col-md-6">
          <div class="gold-selection-panel q-pa-md rounded-borders">
            <!-- Gold Type Selection -->
            <div class="text-subtitle1 q-mb-sm">نوع طلا</div>
            <q-select
              outlined
              v-model="selectedGoldType"
              :options="goldTypeOptions"
              class="q-mb-md gold-select"
              dropdown-icon="expand_more"
              map-options
              emit-value
            />

            <!-- Gold Weight -->
            <div class="text-subtitle1 q-mb-sm">گرم طلا</div>
            <div class="row q-mb-lg">
              <q-input
                outlined
                v-model="goldWeight"
                @update:model-value="updateTomanValue"
                class="col gold-weight-input"
                inputmode="numeric"
                v-persian-numbers
                placeholder="0"
              >
              </q-input>
            </div>

            <!-- Buttons -->
            <div class="row q-gutter-md q-mt-lg">
              <q-btn
                color="positive"
                class="col action-btn"
                label="خرید"
                no-caps
                @click="HandlegoToLoginIdp"
              />
              <q-btn
                color="negative"
                class="col action-btn"
                label="فروش"
                no-caps
                @click="HandlegoToLoginIdp"
              />
            </div>
          </div>
        </div>

        <!-- Right side - Price List -->
        <div class="col-12 col-md-6">
          <div class="q-px-sm">
            <!-- Purchase price -->
            <div
              v-for="item in priceList"
              :key="item.action"
              class="price-item q-mb-md"
            >
              <div class="row items-center">
                <div class="col-5">
                  <div class="text-subtitle1 text-weight-medium q-pl-sm">
                    {{ item.action }}:
                  </div>
                </div>
                <div class="col-7">
                  <div class="price-display">
                    <div
                      v-if="
                        item.action === 'قیمت خرید' ||
                        item.action === 'قیمت فروش'
                      "
                      class="price-value"
                    >
                      <q-input
                        dense
                        borderless
                        v-model="calcolatedPrice"
                        type="text"
                        class="text-h6"
                        v-persian-numbers
                      >
                        <template v-slot:prepend>
                          <span class="text-caption q-pl-sm">تومان</span>
                        </template>
                      </q-input>
                    </div>
                    <div v-else class="price-value">
                      {{ item.price }} <span class="text-caption">تومان</span>
                    </div>
                    <div
                      v-if="item.upValue || item.downValue"
                      class="trend-indicator"
                    >
                      <q-icon
                        :name="item.upValue ? 'arrow_upward' : 'arrow_downward'"
                        :color="item.upValue ? 'positive' : 'negative'"
                        size="sm"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Result Panel (appears after calculation) -->
            <q-card v-if="showResult" class="result-card q-mt-lg q-pa-md">
              <div class="text-subtitle1 text-weight-bold q-mb-sm">
                نتیجه محاسبه:
              </div>
              <div class="row q-col-gutter-md">
                <div class="col-12">
                  <div class="text-h6 text-weight-medium text-center">
                    {{ calculationResult }} تومان
                  </div>
                </div>
              </div>
            </q-card>
          </div>
        </div>

        <!-- Info tooltip -->
        <div class="col-12 q-mt-md">
          <div class="text-caption text-grey-7 flex items-center">
            <q-icon name="info" size="xs" class="q-mr-xs" />
            کارمزد و اجرت بر اساس نرخ قیمت‌های روز محاسبه می‌شود
            <q-tooltip>
              کارمزد: ۰.۱٪ از ارزش طلا
              <br />
              اجرت: بسته به نوع طلا متفاوت است
            </q-tooltip>
          </div>
        </div>
      </div>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import { useWalletStore } from "src/stores/wallet";
import { persianToEnglish } from "src/composable/useNumberUtils";

const useWallet = useWalletStore();

// Gold type options
const goldTypeOptions = [{ label: "طلای آبشده", value: "0" }];
const formatPrice = (value) => {
  if (!value) return "";
  return new Intl.NumberFormat("fa-IR").format(value);
};

// Reactive variables
const selectedGoldType = ref("0");
const goldWeight = ref('');
const showResult = ref(false);
const calculationResult = ref("");
const calcolatedPrice = ref(formatPrice(useWallet.price));

// Price list
const priceList = ref([
  {
    action: "قیمت خرید",
    price: calcolatedPrice.value,
    upValue: true,
    downValue: false,
  },
  {
    action: "قیمت فروش",
    price: useWallet.price,
    upValue: false,
    downValue: true,
  },
  { action: "کارمزد", price: "0" },
  { action: "اجرت", price: "۰" },
  { action: "مالیات", price: "۰" },
]);

const updateTomanValue = (newValue) => {
  const engValue = persianToEnglish(newValue);
  if (engValue) {
    calcolatedPrice.value = formatPrice(
      Number(engValue) * Number(useWallet.price),
    );
  } else {
    calcolatedPrice.value = formatPrice(useWallet.price);
  }
};

const HandlegoToLoginIdp = () => {
  const idpUrl = "http://localhost:9005/login";
  const redirectUri = "http://localhost:9000/authCallBack";
  const callbackUrl = "http://localhost:8080/auth/callback";
  window.location.href = `${idpUrl}?redirect_uri=${encodeURIComponent(redirectUri)}&callback_url=${encodeURIComponent(callbackUrl)}`;
};
</script>

<style scoped>
.calculator-card {
  position: relative;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.98);
}

.gold-selection-panel {
  background: linear-gradient(180deg, var(--q-primary) 10%, var(--q-info) 80%);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.gold-title {
  background: linear-gradient(145deg, var(--q-primary) 60%, var(--q-info) 90%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 16px;
}

.gold-select :deep(.q-field__control) {
  background-color: rgba(255, 255, 255, 0.9);
}

.gold-weight-input :deep(.q-field__control) {
  background-color: rgba(255, 255, 255, 0.9);
}

.price-item {
  padding: 10px 15px;
  border-radius: 8px;
  background-color: #f8f9fa;
  transition: all 0.2s ease;
}

.price-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.price-display {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-value {
  font-weight: 600;
  font-size: 1.1rem;
  direction: rtl;
}

.trend-indicator {
  display: flex;
  align-items: center;
}

.action-btn {
  font-weight: bold;
  border-radius: 8px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.15);
}

.result-card {
  background: linear-gradient(145deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Mobile optimization */
@media (max-width: 600px) {
  .calculator-card {
    padding: 16px !important;
  }

  .gold-title {
    font-size: 1.5rem;
  }

  .price-item {
    padding: 8px 10px;
    margin-bottom: 8px;
  }

  .price-value {
    font-size: 0.9rem;
  }
}
</style>
