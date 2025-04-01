<template>
  <q-page>
    <div class="bg-white q-pa-lg borderDiv">
      <!-- Header with Theme Toggle -->
      <div class="flex column items-center justify-center q-mb-sm">
        <q-icon
          name="mdi-wallet-bifold"
          color="primary"
          size="sm"
          class="q-py-sm"
        />
        <div class="text-h6 text-primary">افزایش اعتبار</div>
      </div>
      <q-separator></q-separator>

      <!-- Main Content -->
      <div class="row q-col-gutter-lg">
        <div class="col-12">
          <!-- Enhanced Tabs -->
          <q-tabs
            v-model="tab"
            class="text-accent q-mb-lg q-pa-sm"
            align="left"
            indicator-color="secondary"
            :breakpoint="600"
            no-caps
          >
            <q-tab
              name="payment"
              label="درگاه پرداخت آنلاین"
              class="text-weight-medium text-subtitle1"
            />
            <q-tab
              name="deposit"
              label="واریز شناسه دار"
              class="text-weight-medium text-subtitle1"
            />
          </q-tabs>

          <!-- Tab Panels with Enhanced Animation -->
          <q-tab-panels
            v-model="tab"
            animated
            transition-prev="slide-right"
            transition-next="slide-left"
          >
            <!-- Online Payment Panel -->
            <q-tab-panel name="payment">
              <q-card flat bordered class="q-pa-lg">
                <!-- Balance and Price Section -->
                <div class="row q-col-gutter-md">
                  <div class="col-12 col-md-6">
                    <div class="text-subtitle1 text-weight-medium q-mb-sm">
                      موجودی کیف پول:
                    </div>
                    <q-input
                      v-persian-numbers
                      outlined
                      readonly
                      v-model="balance"
                      class="balance-input"
                      :type="showBalance ? 'text' : 'password'"
                    >
                      <template v-slot:append>
                        <q-icon
                          :name="showBalance ? 'visibility' : 'visibility_off'"
                          class="cursor-pointer"
                          @click="showBalance = !showBalance"
                          :class="showBalance ? 'text-primary' : 'text-accent'"
                        />
                      </template>
                    </q-input>
                  </div>
                  <div class="col-12 col-md-6">
                    <div class="text-subtitle1 text-weight-medium q-mb-sm">
                      قیمت خرید:
                    </div>
                    <q-input
                      outlined
                      v-persian-numbers
                      readonly
                      v-model="price"
                      class="price-input"
                    >
                      <template v-slot:append>
                        <span class="text-caption">تومان</span>
                      </template>
                    </q-input>
                  </div>
                </div>

                <!-- Enhanced Amount Input -->
                <div class="q-mt-lg">
                  <div class="text-subtitle1 text-weight-medium q-mb-sm">
                    مبلغ افزایش اعتبار (تومان):
                  </div>
                  <q-input
                    outlined
                    v-model="formattedPrice"
                    @update:model-value="handleAmountChange"
                    label="مبلغ را وارد نمایید"
                    :rules="[(val) => !!val || 'لطفا مبلغ را وارد کنید']"
                    lazy-rule
                    v-persian-numbers
                  >
                    <template v-slot:append>
                      <span class="text-caption">تومان</span>
                    </template>
                  </q-input>
                  <div
                    v-if="instantTrading"
                    class="transaction-details q-pa-md"
                  >
                    <div class="detail-row q-mb-lg">
                      <div class="label text-grey-8">گرم دریافتی:</div>
                      <div class="dotted-line"></div>
                      <div class="value text-weight-medium">
                        {{ amountGram }}
                      </div>
                    </div>

                    <div class="detail-row q-mb-lg">
                      <div class="label text-grey-8">کارمزد:</div>
                      <div class="dotted-line"></div>
                      <div class="value text-weight-medium">
                        {{ calculateFee.toLocaleString() }}
                      </div>
                    </div>

                    <div class="detail-row">
                      <div class="labeltext-grey-8">مبلغ نهایی :</div>
                      <div class="dotted-line"></div>
                      <div class="value text-weight-medium">
                        {{ totalAmount.toLocaleString() }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Enhanced Warning Messages -->
                <q-card class="bg-warning-1 q-pa-md q-mt-lg">
                  <div class="row items-center q-gutter-sm">
                    <q-icon name="warning" color="warning" size="sm" />
                    <div class="text-body2">
                      <div>
                        - در فرایند پرداخت، فعالیت مرورگر را متوقف نکنید
                      </div>
                      <div>
                        - خرید از طریق درگاه بانکی فقط با شماره کارت ثبت شده
                        امکان پذیر است
                      </div>
                    </div>
                  </div>
                </q-card>

                <!-- Enhanced Instant Trading Section -->
                <div class="q-mt-lg">
                  <div class="text-h6 text-weight-bold">
                    خرید و فروش لحظه ای
                  </div>
                  <div class="text-body2 q-mb-md text-grey-7">
                    با استفاده از این امکان با افزایش اعتبار کیف پول تومانی
                    موجودی شما در لحظه به طلا تبدیل میگردد
                  </div>
                  <q-toggle
                    v-model="instantTrading"
                    color="primary"
                    label="لینک یکتای تبدیل آنی به طلا"
                  />
                </div>

                <!-- Enhanced Submit Button -->
                <q-btn
                  unelevated
                  color="primary"
                  class="full-width q-mt-lg text-weight-bold"
                  size="lg"
                  :loading="isLoading"
                  @click="handlePayment"
                >
                  <span class="text-subtitle1">به سمت درگاه پرداخت</span>
                  <template v-slot:loading>
                    <q-spinner-dots />
                  </template>
                </q-btn>
              </q-card>
            </q-tab-panel>

            <!-- Bank Deposit Panel -->
            <q-tab-panel name="deposit">
              <q-card flat bordered class="q-pa-lg">
                <!-- Enhanced Company ID Section -->
                <div class="row q-col-gutter-md">
                  <div class="col-12">
                    <div class="text-subtitle1 text-weight-medium q-mb-sm">
                      شماره شما:
                    </div>
                    <q-input
                      outlined
                      readonly
                      v-model="companyId"
                      class="company-id-input"
                    >
                      <template v-slot:append>
                        <q-btn
                          flat
                          round
                          dense
                          icon="content_copy"
                          @click="copyToClipboard(companyId)"
                        >
                          <q-tooltip>کپی شماره</q-tooltip>
                        </q-btn>
                      </template>
                    </q-input>
                    <div class="text-caption text-grey-7 q-mt-sm">
                      شرکت پارا تجارت الکترونیک پنیان
                    </div>
                  </div>
                </div>

                <!-- Enhanced Unique ID Section -->
                <div class="q-mt-lg">
                  <div class="text-subtitle1 text-weight-medium q-mb-sm">
                    شماره یکتا:
                  </div>
                  <q-input
                    outlined
                    readonly
                    v-model="uniqueId"
                    class="unique-id-input"
                  >
                    <template v-slot:append>
                      <q-btn
                        flat
                        round
                        dense
                        icon="content_copy"
                        @click="copyToClipboard(uniqueId)"
                      >
                        <q-tooltip>کپی شماره یکتا</q-tooltip>
                      </q-btn>
                    </template>
                  </q-input>
                </div>

                <!-- Enhanced Warning Box -->
                <q-card class="bg-warning-1 q-pa-md q-mt-lg">
                  <div class="row items-center q-gutter-sm">
                    <q-icon name="info" color="warning" size="sm" />
                    <div class="text-body2">
                      <p class="q-mb-md">
                        برای افزایش اعتبار از طریق واریز شناسه دار کافیست در بخش
                        شرح یا توضیحات تراکنش پایا یا ساتنای بانکی شماره یکتای
                        درج شده را وارد نمایید و عکس رسید خود را بارگذاری کنید.
                      </p>
                      <p class="text-weight-bold q-mb-none">
                        توجه: درصورت عدم ثبت شماره یکتا در بخش شرح یا توضیحات
                        تراکنش، واریز شما برای ما قابل تشخیص نبوده و ممکن است
                        افزایش اعتبار تا ۷۲ ساعت کاری به طول بیانجامد
                      </p>
                    </div>
                  </div>
                </q-card>

                <!-- Enhanced File Upload -->
                <div class="q-mt-lg">
                  <div class="text-subtitle1 text-weight-medium">
                    فایل پیوست
                  </div>
                  <div class="text-caption text-grey-7 q-mb-sm">
                    (JPG, PNG, JPEG) فقط محتوای عکسی
                  </div>
                  <q-uploader
                    url="http://localhost:4444/upload"
                    style="max-width: 100%"
                    accept=".jpg,.jpeg,.png"
                    color="primary"
                    class="custom_uploader"
                    flat
                    bordered
                    :multiple="false"
                    @added="handleFileAdded"
                    @removed="handleFileRemoved"
                  >
                    <template v-slot:header="scope">
                      <div class="row items-center q-pa-sm">
                        <q-btn
                          v-if="scope.canAddFiles"
                          type="a"
                          icon="add_photo_alternate"
                          @click="scope.pickFiles"
                          round
                          dense
                          flat
                        >
                          <q-uploader-add-trigger />
                          <q-tooltip> انتخاب فایل</q-tooltip>
                        </q-btn>
                        <q-spinner v-if="scope.isUploading" class="q-mr-xs" />
                        <div class="col">
                          <div class="text-weight-medium">آپلود تصویر رسید</div>
                          <div class="text-caption text-info">
                            فایل خود را اینجا رها کنید
                          </div>
                        </div>
                      </div>
                    </template>
                  </q-uploader>
                </div>

                <!-- Enhanced Description Input -->
                <div class="q-mt-lg">
                  <div class="text-subtitle1 text-weight-medium q-mb-sm">
                    توضیحات (اختیاری):
                  </div>
                  <q-input
                    v-model="description"
                    outlined
                    type="textarea"
                    rows="4"
                    placeholder="توضیحات خود را وارد کنید..."
                  />
                </div>

                <!-- Enhanced Submit Button -->
                <q-btn
                  unelevated
                  color="primary"
                  class="full-width q-mt-lg text-weight-bold"
                  size="lg"
                  :loading="isLoading"
                  @click="handleSubmit"
                >
                  <span class="text-subtitle1">ارسال</span>
                  <template v-slot:loading>
                    <q-spinner-dots />
                  </template>
                </q-btn>
              </q-card>
            </q-tab-panel>
          </q-tab-panels>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { computed, ref } from "vue";
import { useQuasar } from "quasar";
import { useWalletStore } from "src/stores/wallet";
import { useRouter } from "vue-router";

import { persianToEnglish } from "src/composable/useNumberUtils";
import { api } from "src/boot/axios";

const $q = useQuasar();
const router = useRouter()

// State
const tab = ref("payment");
const amount = ref("");
const instantTrading = ref(false);
const companyId = ref("IR1F806200000030385734500");
const uniqueId = ref("66400483234410");
const description = ref("");
const showBalance = ref(true);
const isLoading = ref(false);
const useWallet = useWalletStore();
const totalAmount = computed(() => {
  const parsedAmount = Number(amount.value);
  return parsedAmount + Number(calculateFee.value);
});

const balance = computed(() => formatPrice(useWallet.balance/10));
const price = computed(() => formatPrice(useWallet.price));
const amountGram = computed(
  () => Number(amount.value) / Number(useWallet.price),
);
const calculateFee = computed(() => Number(amount.value * 0.01));

// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};
// Methods
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    $q.notify({
      message: "کپی شد",
      color: "positive",
      position: "top-right",
      classes: "my_custom_notify",
      timeout: 2000,
      actions: [{ icon: "close", color: "white" }],
    });
  });
};

const handleFileAdded = (files) => {
  $q.notify({
    message: "فایل با موفقیت اضافه شد",
    color: "positive",
    position: "top-right",
    timeout: 2000,
  });
  console.log(files);
};

const handleFileRemoved = () => {
  $q.notify({
    message: "فایل حذف شد",
    color: "warning",
    position: "top",
    timeout: 2000,
  });
};

const handlePayment = async () => {
  if (!amount.value) {
    $q.notify({
      message: "لطفا مبلغ را وارد کنید",
      color: "negative",
      position: "top",
      timeout: 2000,
    });
    return;
  }
  if (!instantTrading.value) {
    try {
      const { data } = await api.post("/rial-deposit", { rial_amount: amount.value *10 });
      console.log(data);
      if(data.success){
        router.push('/dashboard/message')
      }
    } finally {
      isLoading.value = false;
    }
  } else {
    try {
      const { data } = await api.post("/gold-buy", {
        current_price: useWallet.price *10,
        gold_amount: amountGram.value,
        goldis_fee: calculateFee.value * 10,
        final_price: totalAmount.value * 10,
      });
      if(data.success){
        router.push('/dashboard/message')
      }
      console.log(data);
    } finally {
      isLoading.value = false;
    }
  }
};

const handleSubmit = () => {
  $q.dialog({
    title: "تایید ارسال",
    message: "آیا از ارسال اطلاعات اطمینان دارید؟",
    cancel: true,
    persistent: true,
  }).onOk(() => {
    isLoading.value = true;
    setTimeout(() => {
      isLoading.value = false;
      $q.notify({
        message: "اطلاعات با موفقیت ارسال شد",
        color: "positive",
        position: "top",
        timeout: 2000,
      });
    }, 1500);
  });
};

const handleAmountChange = (value) => {
  amount.value = persianToEnglish(value.replace(/,/g, ""));
};

const formattedPrice = computed(() =>
  amount.value ? Number(amount.value).toLocaleString() : "",
);
</script>

<style lang="scss" scoped>
.q-page {
  min-height: 100vh;
  background: var(--q-primary-fade);
}
.borderDiv {
  border-radius: 16px;
}

.transaction-details {
  .detail-row {
    display: flex;
    align-items: center;
    gap: 8px;

    .label {
      white-space: nowrap;
      font-size: 0.95rem;
    }

    .dotted-line {
      flex: 1;
      border: none;
      border-bottom: 2px dotted rgba(0, 0, 0, 0.12);
      margin: 0 8px;
      height: 1px;
    }

    .value {
      white-space: nowrap;
      font-size: 0.95rem;
    }
  }
}

// Enhanced Input Styling
.q-input {
  .q-field__control {
    border-radius: 8px;
    transition: all 0.3s ease;

    &:hover {
      border-color: var(--q-primary);
    }
  }

  &.balance-input,
  &.price-input {
    .q-field__control {
      background: rgba(var(--q-primary-rgb), 0.05);
    }
  }

  &.company-id-input,
  &.unique-id-input {
    .q-field__control {
      background: rgba(var(--q-secondary-rgb), 0.05);
    }
  }
}

// Enhanced Card Styling
.q-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);

  &:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }

  // Warning Card
  &.bg-warning-1 {
    background: rgba(255, 152, 0, 0.08);
    border-color: rgba(255, 152, 0, 0.2);
  }
}

// Enhanced Tab Styling
.q-tabs {
  .q-tab {
    transition: all 0.3s ease;
    border-radius: 8px;
    margin: 0 4px;

    &--active {
      background: rgba(var(--q-primary-rgb), 0.1);
    }

    &:hover {
      background: rgba(var(--q-primary-rgb), 0.05);
    }
  }

  .q-tab__indicator {
    height: 3px;
    border-radius: 3px;
  }
}

// Enhanced Button Styling
.q-btn {
  border-radius: 8px;
  transition: all 0.3s ease;

  &--standard {
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(var(--q-primary-rgb), 0.2);
    }
  }

  // Copy button
  &--round {
    &.flat {
      opacity: 0.7;

      &:hover {
        opacity: 1;
        background: rgba(var(--q-primary-rgb), 0.1);
      }
    }
  }
}

// Enhanced Uploader Styling
.q-uploader {
  border-radius: 12px;
  border: 2px dashed rgba(var(--q-primary-rgb), 0.3);
  transition: all 0.3s ease;

  &:hover {
    border-color: var(--q-primary);
  }

  .q-uploader__header {
    background: transparent;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }

  .q-uploader__list {
    background: rgba(var(--q-primary-rgb), 0.02);
  }
}

// Enhanced Toggle Styling
.q-toggle {
  .q-toggle__inner {
    &:before {
      border-radius: 12px;
    }

    &:after {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
  }

  &--checked {
    .q-toggle__inner {
      &:after {
        box-shadow: 0 2px 8px rgba(var(--q-primary-rgb), 0.3);
      }
    }
  }
}

// Animations
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// Responsive Adjustments
@media (max-width: 600px) {
  .q-card {
    border-radius: 8px;
  }

  .q-btn {
    font-size: 14px;
  }

  .text-h5 {
    font-size: 1.5rem;
  }

  .text-subtitle1 {
    font-size: 1rem;
  }
}
.my_custom_notify {
  padding-right: 20px;
}

// RTL Specific Adjustments
[dir="rtl"] {
  .q-field__control-container {
    padding-right: 8px;
  }

  .q-uploader__header {
    flex-direction: row-reverse;
  }

  .q-btn__content {
    flex-direction: row-reverse;
  }
}

.custom_uploader {
  border: 1px solid var(--q-info);
}
</style>
