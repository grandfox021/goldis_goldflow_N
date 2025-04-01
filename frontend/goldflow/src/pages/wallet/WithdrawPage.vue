<template>
  <q-page>
    <div class="bg-white q-pa-md q-pa-lg-xl borderDiv">
      <!-- Enhanced Header with Icon -->
      <div class="flex column flex-center q-mb-lg">
        <q-icon
          name="account_balance_wallet"
          color="primary"
          size="sm"
          class="q-py-sm"
        />
        <div class="text-h5 text-primary">برداشت از کیف پول</div>
      </div>

      <!-- Progress Stepper -->
      <div class="q-mb-lg">
        <q-stepper
          v-model="step"
          ref="stepper"
          color="primary"
          flat
          active-color="primary"
          alternative-labels
        >
          <q-step
            :name="1"
            title="مبلغ"
            icon="payments"
            :done="step > 1"
            :header-nav="step > 1"
            @click="step = 1"
          />
          <q-step
            :name="2"
            title="روش برداشت"
            icon="transform"
            :done="step > 2"
            :header-nav="step > 2"
            @click="withdrawMethod && step === 2"
          />
          <q-step
            :name="3"
            title="کارت بانکی"
            icon="credit_card"
            :done="step > 3"
            :header-nav="step > 3"
            @click="withdrawMethod && selectedCard && step === 3"
          />
          <q-step :name="4" title="تایید نهایی" icon="done" />
        </q-stepper>
      </div>

      <!-- Main Form Card -->
      <q-card flat bordered class="form-card">
        <q-card-section>
          <!-- Step 1: Amount Selection -->
          <div v-show="step === 1">
            <div class="text-subtitle1 text-weight-bold text-primary q-mb-md">
              مبلغ برداشت
            </div>

            <!-- Quick Amount Selection -->
            <div class="row q-col-gutter-sm q-mb-md">
              <div
                class="col-4 col-sm-3"
                v-for="quickAmount in quickAmounts"
                :key="quickAmount.value"
              >
                <q-btn
                  :label="quickAmount.label"
                  :color="
                    Number(amount) === quickAmount.value ? 'primary' : 'grey-3'
                  "
                  :text-color="
                    Number(amount) === quickAmount.value
                      ? 'secondary'
                      : 'primary'
                  "
                  class="full-width"
                  no-caps
                  unelevated
                  @click="setQuickAmount(quickAmount.value)"
                />
              </div>
            </div>

            <!-- Custom Amount Input -->
            <div class="q-mb-lg">
              <div class="text-subtitle2 text-weight-medium q-mb-sm">
                مبلغ دلخواه (حداقل ۱۰,۰۰۰ تومان):
              </div>
              <q-input
                outlined
                v-model="formattedAmount"
                @update:model-value="handleAmountChange"
                class="custom-input"
                label="مبلغ را وارد نمایید"
                :rules="[
                  (val) => !!val || 'لطفا مبلغ را وارد کنید',
                  (val) =>
                    Number(val.replace(/,/g, '')) >= 10000 ||
                    'حداقل مبلغ برداشت ۱۰,۰۰۰ تومان می‌باشد',
                    (val) =>
                    Number(val.replace(/,/g, '')) <= walletBalance ||
                    'مبلغ وارد شده بیشتر از موجودی است',
                ]"
                lazy-rules
              >
                <template v-slot:prepend>
                  <q-icon name="payments" color="primary" />
                </template>
                <template v-slot:append>
                  <q-btn
                    flat
                    color="primary"
                    label="کل موجودی"
                    class="q-ml-sm"
                    @click="selectAllBalance"
                  />
                </template>
              </q-input>
            </div>

            <!-- Fee Information -->
            <q-card class="info-card q-mb-md">
              <q-card-section class="row items-center no-wrap">
                <q-icon
                  name="info"
                  color="secondary"
                  size="sm"
                  class="q-mr-md"
                />
                <div class="text-body2">
                  کارمزد انتقال: <span class="text-weight-medium">۰ تومان</span>
                </div>
              </q-card-section>
            </q-card>

            <!-- Step Navigation -->
            <div class="row justify-end q-mt-lg">
              <q-btn
                color="primary"
                unelevated
                :disable="!isAmountValid"
                label="ادامه"
                class="q-px-md"
                @click="step = 2"
              />
            </div>
          </div>

          <!-- Step 2: Withdrawal Method -->
          <div v-show="step === 2">
              <!-- Method Selection Cards - Improved Design -->
          <div class="text-subtitle1 text-weight-bold text-primary q-mb-md">
            روش برداشت
          </div>

            <div class="row q-col-gutter-md q-mb-lg">
              <div
                class="col-12 col-sm-6"
                v-for="method in enhancedWithdrawMethods"
                :key="method.value"
              >
                <q-card
                  clickable
                  :class="[
                    'method-card',
                    withdrawMethod === method.value ? 'selected-method' : '',
                  ]"
                  @click="withdrawMethod = method.value"
                >
                  <q-card-section class="row items-center no-wrap">
                    <div class="method-icon-container">
                      <q-icon
                        :name="method.icon"
                        size="md"
                        :color="withdrawMethod === method.value ? 'white' : 'primary'"
                      />
                    </div>
                    <div class="q-ml-md">
                      <div class="text-subtitle2 text-weight-medium">
                        {{ method.label }}
                      </div>
                      <div class="text-caption text-grey-7">
                        {{ method.description }}
                      </div>
                      <div
                        class="text-caption text-primary q-mt-xs"
                        v-if="method.fee"
                      >
                        کارمزد: {{ method.fee }}
                      </div>
                    </div>
                    <q-space />
                    <q-radio
                      v-model="withdrawMethod"
                      :val="method.value"
                      color="primary"
                    />
                  </q-card-section>
                </q-card>
              </div>
            </div>
            <!-- Step Navigation -->
            <div class="row justify-between q-mt-lg">
              <q-btn flat color="grey-7" label="بازگشت" @click="step = 1" />
              <q-btn
                color="primary"
                unelevated
                :disable="!withdrawMethod"
                label="ادامه"
                class="q-px-md"
                @click="step = 3"
              />
            </div>
          </div>

          <!-- Step 3: Card Selection -->
          <div v-show="step === 3">
          <!-- Card Selection - Improved Design -->
          <div class="text-subtitle1 text-weight-bold text-primary q-mb-md">
            انتخاب کارت بانکی
          </div>

          <!-- Display cards if they exist -->
          <div v-if="enhancedBankCards.length !== 0" class="row q-col-gutter-md q-mb-lg">
            <div
              class="col-12 col-md-6"
              v-for="card in enhancedBankCards"
              :key="card.value"
            >
              <q-card
                clickable
                :class="[
                  'card-selection',
                  selectedCard === card.value ? 'selected-card' : '',
                ]"
                @click="selectedCard = card.value"
              >
                <q-card-section>
                  <div class="row items-center no-wrap">
                    <div class="bank-logo-container q-mr-md">
                      <div class="bank-logo">
                        <q-icon
                          name="account_balance"
                          :color="selectedCard === card.value ? 'white' : 'primary'"
                          size="md"
                        />
                      </div>
                    </div>
                    <div class="col">
                      <div class="text-subtitle2 text-weight-medium">
                        {{ card.bankName }}
                      </div>
                      <div dir="rtl" class="text-body2 card-number">
                        <span class="dots">••••</span> <span class="dots">••••</span> <span class="dots">••••</span> <span class="last-digits">{{ card.label.slice(-4) }}</span>
                      </div>
                      <div class="text-caption text-grey-7">
                        {{ card.owner }}
                      </div>
                    </div>
                    <div class="col-auto">
                      <q-radio
                        v-model="selectedCard"
                        :val="card.value"
                        color="primary"
                      />
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <!-- Show add card button if no cards exist -->
          <div v-else class="q-mb-lg text-center">
            <q-btn
              color="primary"
              icon="add_card"
              label="افزودن کارت بانکی"
              no-caps
              rounded
              unelevated
              class="q-px-lg q-py-sm"
              @click="router.push('/dashboard/card')"
            />
            <div class="text-caption text-grey q-mt-sm">
              برای برداشت وجه ابتدا یک کارت بانکی اضافه کنید
            </div>
          </div>

          <!-- Card Information Notice -->
          <q-card class="info-card q-mb-md">
            <q-card-section class="row items-start no-wrap">
              <q-icon
                name="info"
                color="warning"
                size="sm"
                class="q-mr-md q-mt-xs"
              />
              <div>
                <div class="text-body2 text-weight-medium">نکات مهم:</div>
                <ul class="q-mt-xs text-caption text-grey-8">
                  <li>
                    نام صاحب کارت باید با نام شما در سامانه مطابقت داشته باشد.
                  </li>
                  <li>
                    واریز فقط به کارت‌های ثبت شده در پروفایل شما امکان‌پذیر
                    است.
                  </li>
                  <li>
                    زمان واریز به روش پایا حداکثر ۲۴ ساعت و ساتنا حداکثر ۳
                    ساعت می‌باشد.
                  </li>
                </ul>
              </div>
            </q-card-section>
          </q-card>

          <!-- Step Navigation -->
          <div class="row justify-between q-mt-lg">
            <q-btn flat color="grey-7" label="بازگشت" @click="step = 2" />
            <q-btn
              color="primary"
              unelevated
              :disable="!selectedCard && enhancedBankCards.length !== 0"
              label="ادامه"
              class="q-px-md"
              @click="step = 4"
            />
          </div>
        </div>

          <!-- Step 4: Final Confirmation -->
         <div v-show="step === 4">
          <div class="text-h6 text-weight-bold text-primary q-mb-md">
            <q-icon name="done_all" class="q-mr-sm" />
            تایید نهایی
          </div>

    <!-- Improved Withdrawal Summary Card -->
          <q-card class="summary-card q-mb-lg">
            <q-card-section class="summary-header">
              <div class="text-subtitle1 text-weight-medium">
                خلاصه درخواست برداشت
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section class="summary-content">
              <div class="row q-col-gutter-y-md summary-details">
                <!-- Amount -->
                <div class="col-12">
                  <div class="summary-row">
                    <div class="summary-label">
                      <q-icon name="payments" size="xs" class="q-mr-xs" />
                      مبلغ برداشت:
                    </div>
                    <div class="summary-value">
                      <span class="text-weight-medium">{{ formattedAmount }}</span>
                      <span class="text-caption q-ml-xs">تومان</span>
                    </div>
                  </div>
                </div>

                <!-- Method -->
                <div class="col-12">
                  <div class="summary-row">
                    <div class="summary-label">
                      <q-icon name="swap_horiz" size="xs" class="q-mr-xs" />
                      روش برداشت:
                    </div>
                    <div class="summary-value">
                      <q-chip
                        dense
                        outline
                        :color="withdrawMethod === 'satna' ? 'secondary' : 'secondary'"
                        text-color="white"
                        :class="withdrawMethod === 'satna' ? 'bg-info' : 'bg-primary'"
                        size="md"
                      >
                        {{ getMethodLabel }}
                      </q-chip>
                    </div>
                  </div>
                </div>

                <!-- Destination Card -->
                <div class="col-12">
                  <div class="summary-row">
                    <div class="summary-label">
                      <q-icon name="credit_card" size="xs" class="q-mr-xs" />
                      کارت مقصد:
                    </div>
                    <div class="summary-value">
                      <div class="card-info flex">
                        <div class="text-weight-medium bank-name q-pr-sm">{{ getCardBankName }}</div>
                        <div dir="ltr" class="flex text-caption">
                          •••• •••• •••• {{ getCardLastFour }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Fee -->
                <div class="col-12">
                  <div class="summary-row">
                    <div class="summary-label">
                      <q-icon name="account_balance_wallet" size="xs" class="q-mr-xs" />
                      کارمزد:
                    </div>
                    <div class="summary-value">
                      <span :class="getWithdrawFee > 0 ? 'text-negative' : 'text-positive'">
                        {{ getWithdrawFee > 0 ? getWithdrawFee.toLocaleString() + ' تومان' : 'رایگان' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </q-card-section>

            <q-separator />

            <!-- Final Amount Section -->
            <q-card-section class="final-amount-section">
              <div class="row items-center justify-between">
                <div class="text-subtitle1 text-weight-medium">
                  مبلغ نهایی:
                </div>
                <div class="text-h5 text-weight-bold text-primary">
                  {{ getFinalAmount }} <span class="text-caption text-weight-regular q-ml-xs">تومان</span>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Notice Card -->
          <q-card class="notice-card q-mb-md" flat bordered>
            <q-card-section class="row items-start no-wrap">
              <q-icon name="schedule" color="amber-8" size="sm" class="q-mr-sm q-mt-xs" />
              <div>
                <div class="text-body2 text-weight-medium">زمان تقریبی واریز:</div>
                <div class="text-caption q-mt-xs">
                  <span v-if="withdrawMethod === 'paya'">انتقال پایا تا حداکثر ۲۴ ساعت کاری</span>
                  <span v-else-if="withdrawMethod === 'satna'">انتقال ساتنا تا حداکثر ۳ ساعت کاری</span>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Enhanced Terms Checkbox -->
          <q-card class="terms-card q-mb-lg" flat bordered>
            <q-card-section class="row items-center no-wrap">
              <q-checkbox
                v-model="termsAccepted"
                color="primary"
                class="q-mr-md"
                size="md"
              />
              <div>
                <div class="text-body2">
                  شرایط و قوانین برداشت از کیف پول را مطالعه کرده و می‌پذیرم
                </div>
                <div class="text-caption text-primary q-mt-xs cursor-pointer">
                  مشاهده قوانین و مقررات
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Step Navigation -->
          <div class="row justify-between q-mt-xl">
            <q-btn
              flat
              color="grey-7"
              label="بازگشت"
              icon="arrow_back"
              @click="step = 3"
              class="q-px-md"
            />
            <q-btn
              color="primary"
              unelevated
              :disable="!termsAccepted"
              :loading="isLoading"
              icon-right="check_circle"
              label="ثبت درخواست برداشت"
              class="q-px-lg"
              @click="handleWithdrawal"
            >
              <template v-slot:loading>
                <q-spinner-dots />
              </template>
            </q-btn>
          </div>
        </div>
              </q-card-section>
            </q-card>

            <!-- Withdrawal Limits Information -->
            <q-card class="info-card q-mt-lg">
              <q-card-section class="row items-center q-gutter-sm">
                <q-icon name="info" color="info" size="sm" />
                <div class="text-body2">
                  <div class="text-weight-medium">
                    سقف برداشت روزانه:
                    <span class="text-primary">۵۰,۰۰۰,۰۰۰ تومان</span>
                  </div>
                  <div class="text-caption text-grey-7 q-mt-xs">
                    تعداد برداشت در روز: حداکثر ۳ تراکنش
                  </div>
                </div>
              </q-card-section>
           </q-card>
      </div>
  </q-page>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useQuasar } from "quasar";
import { useWalletStore } from "src/stores/wallet";
import { api } from "src/boot/axios";
import { useAuthStore } from "src/stores/auth";
import { useRouter } from "vue-router";
// import { persianToEnglish } from "src/composable/useNumberUtils";

const $q = useQuasar();
const useWallet = useWalletStore();
const authStore = useAuthStore()
const router = useRouter()
// State management
const walletBalance = computed(() =>useWallet.balance/10);
const amount = ref("");
const isLoading = ref(false);
const withdrawMethod = ref("");
const selectedCard = ref("");
const step = ref(1);
const termsAccepted = ref(false);
const cardNumberSelected = computed(() => {
  const number = enhancedBankCards.value.find(c => c.value === selectedCard.value)
  return number
})

// Quick amount selection options
const quickAmounts = [
  { label: "۱۰۰,۰۰۰", value: 100000 },
  { label: "۵۰۰,۰۰۰", value: 500000 },
  { label: "۱,۰۰۰,۰۰۰", value: 1000000 },
  { label: "۲,۰۰۰,۰۰۰", value: 2000000 },
];



// Enhanced withdrawal methods with icons and descriptions
const enhancedWithdrawMethods = [
  {
    label: "انتقال پایا",
    value: "paya",
    icon: "schedule",
    description: "انتقال با تاخیر حداکثر ۲۴ ساعت",
    fee: "رایگان",
  },
  {
    label: "انتقال ساتنا",
    value: "satna",
    icon: "bolt",
    description: "انتقال سریع (حداکثر ۳ ساعت)",
    fee: "۱۰,۰۰۰ تومان",
  },
];

// Enhanced bank cards with logos and owner information
const enhancedBankCards = ref([
]);

// Computed properties
const formattedAmount = computed({
  get: () => (amount.value ? Number(amount.value).toLocaleString() : ""),
  set: (val) => {
    amount.value = val.replace(/,/g, "");
  },
});

const isAmountValid = computed(() => {
  return (
    amount.value &&
    Number(amount.value) >= 10000 &&
    Number(amount.value) <= walletBalance.value
  );
});

const isFormValid = computed(() => {
  return isAmountValid.value && withdrawMethod.value && selectedCard.value;
});

const getMethodLabel = computed(() => {
  const method = enhancedWithdrawMethods.find(
    (m) => m.value === withdrawMethod.value,
  );
  return method ? method.label : "";
});



// Methods
const handleAmountChange = (value) => {
  amount.value = value.replace(/,/g, "");
};

const selectAllBalance = () => {
  amount.value = Number(walletBalance.value);
  formattedAmount.value = amount.value.toLocaleString();
};

const setQuickAmount = (quickAmount) => {
  amount.value = quickAmount.toString();
  formattedAmount.value = quickAmount.toLocaleString();
};


const handleWithdrawal = async() => {
  if (!isFormValid.value || !termsAccepted.value) {
    $q.notify({
      message: "لطفا تمام فیلدها را به درستی پر کنید",
      color: "negative",
      position: "top",
      timeout: 2000,
    });
    return;
  }

  isLoading.value = true;

  try{
    const { data } = await api.post('/create-withdrawl-request', {
      card_number : cardNumberSelected.value.label,
      amount : Number(amount.value) * 10
    })
    console.log(data)
    if(data.success === true){
        router.push('/dashboard/message')
      }
  }finally{
    // Reset form
    amount.value = "";
    step.value = 1;
    termsAccepted.value = false;

    walletBalance.value -= Number(amount.value);
  ;
  }


};

 // bank name
 const bankBins = {
  // بانک ملی ایران
  603799: "بانک ملی ایران",
  170019: "بانک ملی ایران (نوع سپرده)",

  // بانک صادرات ایران
  603769: "بانک صادرات ایران",

  // بانک سپه (و بانک‌های ادغامی در آن: انصار، حکمت ایرانیان، قوامین، مهر اقتصاد)
  589210: "بانک سپه",
  627648: "بانک سپه (قدیم)، یا بانک انصار (سابق)",
  639599: "بانک سپه (سابقاً قوامین)",
  504172: "بانک سپه (سابقاً رسالت/حکمت/...)", // امکان تداخل با بانک رسالت هم وجود دارد
  505801: "بانک سپه (سابقاً کوثر/مهراقتصاد)",

  // بانک تجارت
  627353: "بانک تجارت",
  585983: "بانک تجارت",

  // بانک ملت
  610433: "بانک ملت",
  991975: "بانک ملت",
  991976: "بانک ملت",

  // بانک کشاورزی
  603770: "بانک کشاورزی",

  // بانک مسکن
  628023: "بانک مسکن",

  // بانک سامان
  621986: "بانک سامان",

  // بانک پارسیان
  622106: "بانک پارسیان",
  627884: "بانک پارسیان",

  // بانک پاسارگاد
  502229: "بانک پاسارگاد",
  639347: "بانک پاسارگاد",

  // بانک توسعه صادرات
  627344: "بانک توسعه صادرات",

  // بانک آینده
  636214: "بانک آینده",
  636949: "بانک آینده (برخی کارت‌های حکمت سابق)",

  // بانک سرمایه
  639607: "بانک سرمایه",

  // بانک شهر
  502806: "بانک شهر",
  504706: "بانک شهر",

  // پست بانک ایران
  627760: "پست بانک ایران",

  // بانک دی
  502938: "بانک دی",

  // بانک اقتصاد نوین
  627412: "بانک اقتصاد نوین",

  // بانک انصار (سابق) -> ادغام در سپه
  // '627381': 'بانک انصار (ادغام در بانک سپه)',

  // مؤسسه اعتباری توسعه (قدیمی) یا موارد متفرقه
  // '628157': 'موسسه اعتباری توسعه',
  // ...

  // بانک گردشگری
  505416: "بانک گردشگری",

  // بانک ایران زمین
  505785: "بانک ایران زمین",

  // بانک مهر ایران (قرض‌الحسنه مهر)
  606373: "بانک قرض‌الحسنه مهر ایران",
};

const fetchCardsData = async() => {
  const { data } = await api.get('/get-card-number')
  const cleanCard = data.card_number.toString()
  const bin = cleanCard.substring(0,6)
  const bankLabel = bankBins[bin] || 'نامشخص'
 console.log(data.card_number);
 const newCard = {
      label: data.card_number.toString(),
      value: `${cleanCard.slice(-4)}`, // Create a unique ID using last 4 digits
      bankName: bankLabel,
      owner: authStore.firstName,
    };
  console.log(newCard)
  enhancedBankCards.value = [newCard]
  console.log(enhancedBankCards)
}

watch(() => {
  if(step.value === 3){
    fetchCardsData()
  }
  if(step.value === 4){
    console.log('this is amount', amount.value* 10)
  }
})

// Get card bank name only
const getCardBankName = computed(() => {
  const card = enhancedBankCards.value.find((c) => c.value === selectedCard.value);
  return card ? card.bankName : "";
});

// Get card last four digits
const getCardLastFour = computed(() => {
  const card = enhancedBankCards.value.find((c) => c.value === selectedCard.value);
  return card ? card.label.slice(-4) : "";
});

// Get withdraw fee based on method
const getWithdrawFee = computed(() => {
  if (withdrawMethod.value === 'satna') {
    return 10000;
  }
  return 0;
});

// Calculate final amount
const getFinalAmount = computed(() => {
  if (!amount.value) return "0";
  const finalAmount = Number(amount.value) - getWithdrawFee.value;
  return finalAmount.toLocaleString();
});
</script>

<style lang="scss" scoped>
.q-page {
  min-height: 100vh;
  background: #f5f8fa;
}

.borderDiv {
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

/* Card styling */
.balance-card,
.form-card,
.info-card,
.summary-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
}

.balance-card {
  background: linear-gradient(
    to left,
    rgba(var(--q-primary-rgb), 0.05),
    rgba(var(--q-primary-rgb), 0.02)
  );

  .balance-container {
    background: white;
    padding: 8px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  }

  .balance-value {
    display: flex;
    align-items: center;
  }
}

.info-card {
  background: rgba(33, 150, 243, 0.05);
  border-color: rgba(33, 150, 243, 0.1);
}

.summary-card {
  .summary-details {
    border-top: 1px solid rgba(0, 0, 0, 0.05);
    padding-top: 12px;
  }
}

/* Method selection styling */
.method-card {
  transition: all 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.08);

  &.selected-method {
    border-color: var(--q-primary);
    background: rgba(var(--q-primary-rgb), 0.05);
    box-shadow: 0 4px 8px rgba(var(--q-primary-rgb), 0.1);
    transform: translateY(-2px);
  }

  &:hover:not(.selected-method) {
    border-color: rgba(var(--q-primary-rgb), 0.3);
  }
}

/* Card selection styling */
.card-selection {
  transition: all 0.2s ease;
  border: 1px solid rgba(0, 0, 0, 0.08);

  &.selected-card {
    border-color: var(--q-primary);
    background: rgba(var(--q-primary-rgb), 0.05);
    box-shadow: 0 4px 8px rgba(var(--q-primary-rgb), 0.1);
  }

  &:hover:not(.selected-card) {
    border-color: rgba(var(--q-primary-rgb), 0.3);
  }

  &.dashed-card {
    border: 1px dashed rgba(0, 0, 0, 0.15);
    background: rgba(0, 0, 0, 0.02);

    &:hover {
      background: rgba(0, 0, 0, 0.04);
    }
  }
}

/* Input field styling */
.custom-input {
  .q-field__control {
    border-radius: 8px;

    &:hover {
      border-color: var(--q-primary);
    }
  }
}

/* Button styling */
.q-btn {
  border-radius: 8px;
  font-weight: 500;

  &.q-btn--standard {
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;

    &:not(.q-btn--round):hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 8px rgba(var(--q-primary-rgb), 0.25);
    }
  }
}

/* Stepper styling */
.q-stepper {
  background: transparent;

  .q-stepper__tab {
    &--active,
    &--done {
      color: var(--q-primary);

      .q-stepper__dot {
        background: var(--q-primary);
      }
    }
  }
}

/* Notification styling */
.notification-success {
  background: #4caf50;
  color: white;
  font-weight: 500;
}

/* Responsive adjustments */
@media (max-width: 599px) {
  .borderDiv {
    border-radius: 0;
    box-shadow: none;
  }

  .q-stepper__tab {
    padding: 8px;

    .q-stepper__label {
      font-size: 12px;
    }
  }

  .q-btn {
    font-size: 14px;
  }
}
/* Method card styling - Improved */
.method-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  position: relative;

  &.selected-method {
    border-color: var(--q-primary);
    background: linear-gradient(to right, rgba(var(--q-primary-rgb), 0.05), rgba(var(--q-primary-rgb), 0.08));
    box-shadow: 0 4px 12px rgba(var(--q-primary-rgb), 0.15);
    transform: translateY(-2px);

    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--q-primary);
    }
  }

  &:hover:not(.selected-method) {
    border-color: rgba(var(--q-primary-rgb), 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .method-icon-container {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(var(--q-primary-rgb), 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }

  &.selected-method .method-icon-container {
    background: var(--q-primary);
  }
}

/* Card selection styling - Improved */
.card-selection {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  position: relative;

  &.selected-card {
    border-color: var(--q-primary);
    background: linear-gradient(to right, rgba(var(--q-primary-rgb), 0.05), rgba(var(--q-primary-rgb), 0.08));
    box-shadow: 0 4px 12px rgba(var(--q-primary-rgb), 0.15);
    transform: translateY(-2px);

    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--q-primary);
    }
  }

  &:hover:not(.selected-card) {
    border-color: rgba(var(--q-primary-rgb), 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .bank-logo-container {
    .bank-logo {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(var(--q-primary-rgb), 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }
  }

  &.selected-card .bank-logo {
    background: var(--q-primary);
  }

  .card-number {
    direction: rtl;
    text-align: right;
    font-family: monospace;
    letter-spacing: 1px;

    .dots {
      color: #777;
    }

    .last-digits {
      font-weight: bold;
      color: var(--q-primary);
    }
  }

  &.dashed-card {
    border: 1px dashed rgba(var(--q-primary-rgb), 0.3);
    background: rgba(var(--q-primary-rgb), 0.02);

    &:hover {
      background: rgba(var(--q-primary-rgb), 0.05);
      box-shadow: 0 2px 8px rgba(var(--q-primary-rgb), 0.1);
    }
  }
}

.summary-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);

  .summary-header {
    background: rgba(var(--q-primary-rgb), 0.03);
    padding: 16px;
  }

  .summary-content {
    padding: 16px;
  }

  .summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;

    &:not(:last-child) {
      border-bottom: 1px dashed rgba(0, 0, 0, 0.05);
    }
  }

  .summary-label {
    display: flex;
    align-items: center;
    color: var(--q-grey-7);
  }

  .summary-value {
    display: flex;
    align-items: center;
  }

  .card-info {
    text-align: left;

    .bank-name {
      font-size: 0.9rem;
    }

    .card-number {
      direction: ltr;
      font-family: monospace;
      letter-spacing: 1px;
      color: var(--q-grey-7);
    }
  }

  .final-amount-section {
    background: linear-gradient(to left, rgba(var(--q-primary-rgb), 0.05), rgba(var(--q-primary-rgb), 0.02));
    padding: 16px;
  }
}

/* Notice card styling */
.notice-card {
  border-radius: 12px;
  background: rgba(255, 193, 7, 0.05);
  border-color: rgba(255, 193, 7, 0.2) !important;
}

/* Terms card styling */
.terms-card {
  border-radius: 12px;
  background: rgba(var(--q-primary-rgb), 0.02);
  border-color: rgba(var(--q-primary-rgb), 0.1) !important;

  .text-caption.text-primary {
    text-decoration: underline;
    text-underline-offset: 2px;

    &:hover {
      opacity: 0.8;
    }
  }
}

/* Button styling enhancements */
.q-btn {
  &.q-btn--standard.q-btn--rectangle {
    border-radius: 12px;

    &[color="primary"] {
      font-weight: 500;
      letter-spacing: 0.5px;

      &:not(:disabled):hover {
        box-shadow: 0 6px 12px rgba(var(--q-primary-rgb), 0.25);
        transform: translateY(-2px);
      }
    }
  }
}
</style>
