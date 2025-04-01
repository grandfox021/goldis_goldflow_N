<template>
  <q-page class="trading-page">
    <div class="content-wrapper">
      <div class="div-style">
        <!-- Glass-morphic Stats Cards -->

        <!--  Trading Interface -->
        <div class="trading-interface q-pa-sm orderStyle1 q-mb-sm">
          <q-tabs
            v-model="activeTab"
            class="custom-tabs"
            active-color="primary"
            indicator-color="secondary"
            align="justify"
            narrow-indicator
          >
            <q-tab name="buy" class="custom-tab">
              <q-icon name="shopping_cart" size="24px" />
              <span class="q-ml-sm">خرید طلای آبشده</span>
            </q-tab>
            <q-tab name="sell" class="custom-tab">
              <q-icon name="sell" size="24px" />
              <span class="q-ml-sm">فروش طلای آبشده</span>
            </q-tab>
          </q-tabs>

          <q-separator color="info" />

          <q-tab-panels
            v-model="activeTab"
            animated
            transition-prev="slide-right"
            transition-next="slide-left"
          >
            <q-tab-panel name="buy">
              <q-form @submit.prevent="handleDialogFactor">
              <div class="row q-col-gutter-sm">

                  <div class="col-12 col-md-6">
                    <!-- Rules Banner -->
                  <div class="rules-banner q-mb-lg" @click="showModal = true">
                    <q-icon name="gavel" color="primary" size="28px" />
                    <div class="rules-content">
                      <div class="text-weight-medium">
                        قوانین و مقررات معاملات
                      </div>
                      <div class="text-caption">
                        لطفاً قبل از انجام معامله، قوانین را مطالعه کنید
                      </div>
                    </div>
                  </div>

                  <!-- Amount Inputs -->
                  <div class="input-group q-mb-lg">
                    <label class="input-label ">میزان طلا</label>
                    <q-input
                      v-model="formattedAmount"
                      @update:model-value="updateAmountValue"
                      outlined
                      class="modern-input text-h6"
                      v-persian-numbers
                      :rules="[
                        (val) =>
                          validateAmountPrecision(val) ||
                          'مقدار باید حداکثر ۸ رقم اعشار داشته باشد',
                      ]"
                    >
                      <template v-slot:prepend>
                        <q-icon name="scale" color="primary q-pl-sm" />
                      </template>
                      <template v-slot:append>
                        <q-btn-dropdown
                          flat
                          color="primary"
                          :label="selectUnit"
                        >
                          <q-list>
                            <q-item
                              clickable
                              v-close-popup
                              @click="handleSelectedUnitGram"
                            >
                              <q-item-section>گرم</q-item-section>
                            </q-item>
                            <q-item
                              clickable
                              v-close-popup
                              @click="handleSelectedUnitSoat"
                            >
                              <q-item-section>سوت</q-item-section>
                            </q-item>
                          </q-list>
                        </q-btn-dropdown>
                      </template>
                    </q-input>
                    <div class="input-hint">
                      <q-icon name="info" size="16px" />
                      حداقل میزان خرید: ۰.۱ گرم
                    </div>
                  </div>

                  <div class="input-group">
                    <label class="input-label">مبلغ (تومان)</label>
                    <q-input
                      v-model="formattedToman"
                      @update:model-value="updateTomanValue"
                      outlined
                      class="modern-input text-h6 text-accent"
                      v-persian-numbers
                      :rules="[validateInput]"
                    >
                      <template v-slot:prepend>
                        <q-icon name="payments" color="primary q-pl-sm" />
                      </template>
                      <template v-slot:append>
                        <q-btn
                        label="کل موجودی"
                        color="primary"
                        class="balance-btn"
                        @click="handleBalanceInput"
                        />
                      </template>
                    </q-input>
                  </div>


                </div>

                <div class="col-12 col-md-6">
                  <!-- Transaction Summary -->
                  <div class="summary-card">
                    <!-- current price input  -->
                    <div class="q-mb-sm">
                      <q-input
                      readonly
                      class="bg-dark modern-input"
                      >
                      <template v-slot:prepend>
                        <span class="text-subtitle1 q-px-sm">قیمت خرید :</span>
                      </template>
                      <template v-slot:append>
                        <span class="text-primary text-subtitle3 q-px-sm">{{ formatPrice(currentPrice) }}</span>
                      </template>

                      </q-input>
                     </div>
                    <h2 class="text-h6 q-mb-lg">جزئیات تراکنش</h2>
                    <div class="summary-item">
                      <span>موجودی کیف پول</span>
                      <span>{{ formatPrice(balance) }} تومان</span>
                    </div>
                    <div class="summary-item">
                      <span>کارمزد خرید</span>
                      <span
                        >{{ Number(calculateFee).toLocaleString() }} تومان</span
                      >
                    </div>
                    <div class="summary-item">
                      <span>هزینه بیمه و نگهداری</span>
                      <span>۱۰,۰۰۰ تومان</span>
                    </div>
                    <q-separator class="q-my-lg" />
                    <div class="summary-total">
                      <span>مبلغ قابل پرداخت</span>
                      <span class="total-amount"
                        >{{ totalAmount.toLocaleString() }} تومان</span
                      >
                    </div>

                    <!-- Payment Options -->
                    <div class="payment-options">
                      <q-btn
                        outline
                        color="primary"
                        class="payment-button"
                        type="submit"
                      >
                        <q-icon
                          name="account_balance_wallet"
                          size="24px"
                          class="q-pl-sm"
                        />
                        <span class="q-ml-sm">پرداخت از کیف پول</span>
                      </q-btn>
                    </div>
                  </div>
                </div>

              </div>
            </q-form>
            </q-tab-panel>

            <q-tab-panel name="sell">
              <q-form @submit.prevent="handleDialogReciept">
                <div class="row q-col-gutter-xl">
                <div class="col-12 col-md-6">
                   <!-- Rules Banner -->
                   <div class="rules-banner q-mb-lg" @click="showModal = true">
                    <q-icon name="gavel" color="secondary" size="28px" />
                    <div class="rules-content">
                      <div class="text-weight-medium">
                        قوانین و مقررات معاملات
                      </div>
                      <div class="text-caption">
                        لطفاً قبل از انجام معامله، قوانین را مطالعه کنید
                      </div>
                    </div>
                  </div>


                  <!-- Amount Inputs -->
                  <div class="input-group q-mb-lg">
                    <label class="input-label">میزان طلا</label>
                    <q-input
                      v-model="formattedAmount"
                      @update:model-value="updateAmountValue"
                      outlined
                      class="modern-input text-h6"
                      v-persian-numbers
                      :rules="[
                        (val) =>
                          validateAmountPrecision(val) ||
                          'مقدار باید حداکثر ۸ رقم اعشار داشته باشد',
                      ]"
                    >
                      <template v-slot:prepend>
                        <q-icon name="scale" color="secondary q-pl-sm" />
                      </template>
                      <template v-slot:append>
                        <q-btn-dropdown
                          flat
                          color="secondary"
                          :label="selectUnit"
                        >
                          <q-list>
                            <q-item
                              clickable
                              v-close-popup
                              @click="handleSelectedUnitGram"
                            >
                              <q-item-section>گرم</q-item-section>
                            </q-item>
                            <q-item
                              clickable
                              v-close-popup
                              @click="handleSelectedUnitSoat"
                            >
                              <q-item-section>سوت</q-item-section>
                            </q-item>
                          </q-list>
                        </q-btn-dropdown>
                      </template>
                    </q-input>
                    <div class="input-hint">
                      <q-icon name="info" size="16px" />
                      حداقل میزان خرید: ۰.۱ گرم
                    </div>
                  </div>

                  <div class="input-group">
                    <label class="input-label">مبلغ (تومان)</label>
                    <q-input
                      v-model="formattedToman"
                      @update:model-value="updateTomanValue"
                      outlined
                      class="modern-input text-h6"
                      v-persian-numbers
                      :rules="[validateInput]"
                    >
                      <template v-slot:prepend>
                        <q-icon name="payments" color="secondary q-pl-sm" />
                      </template>
                      <template v-slot:append>
                        <q-btn
                        label="کل موجودی"
                        color="secondary"
                        class="balance-btn"
                        @click="handleBalanceInput"
                        />
                      </template>
                    </q-input>
                  </div>

                </div>

                <div class="col-12 col-md-6">
                  <!-- Transaction Summary -->
                  <div class="summary-card">
                    <!-- current price input  -->
                   <div class="q-mb-sm">
                      <q-input
                      readonly
                      class="bg-dark modern-input"
                      >
                      <template v-slot:prepend>
                        <span class="text-subtitle1 q-pl-sm">قیمت فروش :</span>
                      </template>
                      <template v-slot:append>
                        <span class="text-secondary text-subtitle3 q-px-sm">{{ formatPrice(currentPrice) }}</span>
                      </template>

                      </q-input>
                     </div>
                    <h2 class="text-h6 q-mb-lg">جزئیات تراکنش</h2>
                    <div class="summary-item">
                      <span>موجودی کیف پول</span>
                      <span>{{ formatPrice(balance) }} تومان</span>
                    </div>
                    <div class="summary-item">
                      <span>کارمزد خرید</span>
                      <span
                        >{{ Number(calculateFee).toLocaleString() }} تومان</span
                      >
                    </div>
                    <div class="summary-item">
                      <span>هزینه بیمه و نگهداری</span>
                      <span>۱۰,۰۰۰ تومان</span>
                    </div>
                    <q-separator class="q-my-lg" />
                    <div class="summary-total">
                      <span>مبلغ قابل پرداخت</span>
                      <span class="total-amount text-secondary"
                        >{{ totalAmount.toLocaleString() }} تومان</span
                      >
                    </div>

                    <!-- Payment Options -->
                    <div class="payment-options">
                      <q-btn
                        outline
                        color="secondary"
                        class="payment-button"
                        type="submit"
                      >
                        <q-icon
                          name="account_balance_wallet"
                          size="24px"
                          class="q-pl-sm"
                        />
                        <span class="q-ml-sm">واریز به کیف پول</span>
                      </q-btn>
                    </div>
                  </div>
                </div>
              </div>
              </q-form>
            </q-tab-panel>
          </q-tab-panels>
        </div>
      </div>
    </div>
    <rulesPopUp v-model="showModal" />
    <factorDialog v-model="showFactor" :data="data" :start="startCounting"/>
    <RecieptDialogDeposite v-model="showReciept" :data="data" :start="startCounting" />
  </q-page>
</template>

<script setup>
import { ref, computed, watch, reactive, defineAsyncComponent } from "vue";
import { persianToEnglish } from "src/composable/useNumberUtils";
import { englishToPersian } from "src/composable/useNumberUtils";
import { useWalletStore } from "src/stores/wallet";
import { validateInput } from "src/rules/rules";
import { useRoute } from "vue-router";

const rulesPopUp = defineAsyncComponent(() => import('src/components/dashboard/rulesPopUp.vue'))
const factorDialog = defineAsyncComponent(() => import('src/components/dashboard/factorDialog.vue'))
const RecieptDialogDeposite = defineAsyncComponent(() => import('src/components/dashboard/RecieptDialogDeposite.vue'))
const balance = computed(() => useWallet.balance/10 )

const showReciept = ref(false)
const activeTab = ref("buy");
const currentPrice = computed(() => useWallet.price)
const selectUnit = ref("سوت");
const showModal = ref(false);
const showFactor = ref(false);
const amount = ref("");
const price = ref("");
const useWallet = useWalletStore()
const route = useRoute()
const selectedAmount = ref(route.query.data)
const startCounting = ref(false)

// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};

const validateAmountPrecision = (value) => {

  // بررسی تعداد ارقام اعشار (حداکثر ۸ رقم اعشار مجاز است)
  const decimalPart = value.toString().includes(".")
    ? persianToEnglish(value.toString().split(".")[1])
    : "";
  if (decimalPart.length > 8) {
    return false;

  }

  return true;
};

watch(() => selectedAmount.value, (newValue) => {
  if(newValue){
    amount.value = newValue
    price.value = amount.value * currentPrice.value / 1000
  }
}, { immediate: true })

function handleDialogFactor(){
  showFactor.value = true
  startCounting.value = true
}
function handleDialogReciept(){
  showReciept.value = !showReciept.value
  startCounting.value = true
}

function handleBalanceInput(){
  const walletFee = (Number(balance.value) - 10000)* 0.1
  const finalPrice = Number(balance.value) - 10000 - walletFee
  price.value = finalPrice
  if(selectUnit.value === 'سوت'){
    amount.value = englishToPersian(
      ((Number(finalPrice) / currentPrice.value) * 1000).toFixed(2),
    );
  }else{
    amount.value = englishToPersian((Number(finalPrice) / currentPrice.value).toFixed(2))
  }
}

function handleSelectedUnitGram() {
  selectUnit.value = "گرم";
  price.value = "";
  amount.value = "";
}
function handleSelectedUnitSoat() {
  selectUnit.value = "سوت";
  price.value = "";
  amount.value = "";
}

const formattedAmount = computed(() => {
  return englishToPersian(amount.value);
});

const formattedToman = computed(() =>
  price.value ? englishToPersian(Number(price.value).toLocaleString()) : "",
);


function updateAmountValue(newValue) {
  const englishValue = persianToEnglish(newValue);
  amount.value = englishValue;

  if (englishValue && selectUnit.value === "سوت") {
    price.value = ((Number(englishValue) * currentPrice.value) / 1000).toFixed(
      1,
    );
  } else if (englishValue && selectUnit.value === "گرم") {
    price.value = (Number(englishValue) * currentPrice.value).toFixed(1);
  } else {
    price.value = "";
  }
}

function updateTomanValue(newValue) {
  const englishValue = persianToEnglish(newValue);
  const cleanValue = englishValue.replace(/[^\d.]/g, "");
  price.value = cleanValue;

  if (cleanValue && selectUnit.value === "سوت") {
    amount.value = englishToPersian(
      ((Number(cleanValue) / currentPrice.value) * 1000).toFixed(1),
    );
  } else if (cleanValue && selectUnit.value === "گرم") {
    amount.value = englishToPersian(
      (Number(cleanValue) / currentPrice.value).toFixed(1),
    );
  } else {
    amount.value = "";
  }
}

const amountInGrams = computed(() => {
  return selectUnit.value === "سوت"
    ? persianToEnglish(amount.value) / 1000
    : persianToEnglish(amount.value);
});

const calculateFee = computed(() => {
  return amountInGrams.value
    ? Math.round(amountInGrams.value * currentPrice.value * 0.01)
    : 0;
});

const totalAmount = computed(() => {
  const baseAmount = amountInGrams.value
    ? amountInGrams.value * currentPrice.value
    : 0;
  return baseAmount + calculateFee.value + 10000;
});


const data = reactive({
  totalAmount: 0,
  amountInGrams: 0,
  calculateFee: 0,
  currentPrice: 0,
});

watch(
  [totalAmount, amountInGrams, calculateFee,currentPrice],
  ([newTotal, newAmount, newFee,newPrice]) => {
    data.totalAmount = newTotal;
    data.amountInGrams = newAmount;
    data.calculateFee = newFee;
    data.currentPrice = newPrice
  },
);
watch(showFactor, (newValue) => {
  if (newValue) {
    data.totalAmount = totalAmount.value;
    data.amountInGrams = amountInGrams.value;
    data.calculateFee = calculateFee.value;
    data.currentPrice = currentPrice.value;
  }
});
</script>

<style scoped>
.balance-btn{
  border-radius: 6px;
}
.div-style {
  display: flex;
  flex-direction: column;
}

.trading-page {
  min-height: 100vh;
  background: #f8fafc;
}

.background-pattern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 400px;
  background: linear-gradient(135deg, var(--q-primary) 80%, #2c5282 100%);
  z-index: 0;
}

.gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(180deg, transparent 0%, #f8fafc 100%);
}

.content-wrapper {
  position: relative;
  z-index: 1;
}

.header-container {
  padding: 2rem 0;
}

.user-profile {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px -2px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  background: rgba(var(--q-primary-rgb), 0.1);
  color: var(--q-primary);
  padding: 1rem;
  border-radius: 12px;
  transition: transform 0.2s;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1);
}

.stat-icon.secondary {
  background: rgba(var(--q-secondary-rgb), 0.1);
  color: var(--q-secondary);
}

.stat-icon.accent {
  background: rgba(var(--q-accent-rgb), 0.1);
  color: var(--q-accent);
}

.stat-content {
  flex: 1;
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.stat-change {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change .period {
  color: #64748b;
  margin-right: 0.5rem;
}

.trading-interface {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}

.custom-tabs {
  padding: 0.5rem;
}

.custom-tab {
  padding-top: 5px;
  padding-bottom: 5px;
  font-weight: 500;
  transition: background-color 0.2s;
  border-radius: 12px;
}

.custom-tab:hover {
  background: rgba(var(--q-primary-rgb), 0.05);
}

.rules-banner {
  background: rgba(var(--q-primary-rgb), 0.05);
  border: 1px solid rgba(var(--q-primary-rgb), 0.1);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.rules-banner:hover {
  background: rgba(var(--q-primary-rgb), 0.08);
  transform: translateY(-1px);
}

.rules-content {
  flex: 1;
}



.input-label {
  display: block;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.modern-input {
  border-radius: 12px;
}

.modern-input :deep(.q-field__control) {
  height: 56px;
  border-radius: 12px;
}

.modern-input :deep(.q-field__control:before) {
  border: 2px solid #e2e8f0;
}

.modern-input :deep(.q-field__control:hover:before) {
  border-color: var(--q-primary);
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
  margin-top: 0.1rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 1.5rem;
  height: 100%;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  color: #64748b;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  font-weight: 600;
  color: #1e293b;
}

.total-amount {
  font-size: 1.25rem;
  color: var(--q-primary);
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.payment-button {
  width: 100%;
  height: 56px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.2s;
}

.payment-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.wallet-btn {
  margin-top: 0.5rem;
  border-radius: 8px;
  font-size: 0.875rem;
}


/* Responsive Adjustments */
@media (max-width: 1024px) {

  .header-container {
    padding: 1rem 0;
  }

  .stat-card {
    padding: 1rem;
  }

  .trading-interface {
    padding: 0.2rem;
  }
}

@media (max-width: 600px) {
  .background-pattern {
    height: 300px;
  }

  .user-profile {
    padding: 0.75rem;
  }

  .stat-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .payment-options {
    flex-direction: column;
  }

  .payment-button {
    width: 100%;
  }
}
</style>
