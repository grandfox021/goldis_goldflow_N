<template>
  <q-dialog v-model="show" persistent class="payment-dialog">
    <q-card class="modern-payment-card">
      <!-- Header with gradient background -->
      <q-card-section class="gradient-header text-white q-pa-md bg-secondary">
        <div class="row items-center justify-between">
          <div class="text-h5 text-weight-medium">خرید طلای آبشده</div>
          <q-btn flat round icon="close" color="white" v-close-popup @click="resetCountDown">
            <q-tooltip>بستن</q-tooltip>
          </q-btn>
        </div>
      </q-card-section>

      <!-- Timer Banner -->
      <div class="timer-banner q-px-md q-py-sm row items-center justify-center">
        <q-icon name="timer" size="20px" color="amber-9" class="q-mr-sm" />
        <span class="text-amber-9"
          >{{ countdown }} ثانیه تا انقضای پیش فاکتور</span
        >
      </div>

      <!-- Main Content -->
      <q-card-section class="content-section q-pt-lg">
        <!-- Price Card -->
        <div class="price-summary-card q-pa-lg q-mb-lg">
          <div class="row items-center justify-between">
            <div class="text-subtitle1 text-grey-8">قیمت فعلی هر گرم</div>
            <div class="text-h5 text-weight-medium">
              {{ formatNumber(props.data.currentPrice) }}
              <span class="text-body2 q-ml-sm">تومان</span>
            </div>
          </div>
          <q-linear-progress
            rounded
            size="2px"
            color="primary"
            class="q-mt-md"
            value="1"
          />
        </div>

        <!-- Transaction Details Card -->
        <div class="details-card q-pa-md">
          <div class="text-subtitle1 text-weight-medium q-pb-md">
            جزییات تراکنش
          </div>

          <!-- Amount Row -->
          <div class="detail-row">
            <div class="row items-center justify-between q-py-md">
              <div class="detail-label">میزان خرید</div>
              <div class="detail-value">
                <span class="amount unit-badge">{{
                  props.data.amountInGrams
                }}</span>
                <span class="unit">گرم</span>
              </div>
            </div>
          </div>

          <!-- Storage Fee Row -->
          <div class="detail-row">
            <div class="row items-center justify-between q-py-md">
              <div class="detail-label">هزینه نگهداری</div>
              <div class="detail-value">
                <span class="amount unit-badge">{{ fee }}</span>
                <span class="q-ml-sm">هزار تومان ماهیانه</span>
              </div>
            </div>
          </div>

          <!-- Commission Row -->
          <div class="detail-row">
            <div class="row items-center justify-between q-py-md">
              <div class="detail-label">کارمزد معامله</div>
              <div class="detail-value">
                <span class="amount unit-badge">{{
                  formatNumber(props.data.calculateFee)
                }}</span>
                <span class="q-ml-sm">تومان</span>
              </div>
            </div>
          </div>

          <!-- Total Amount -->
          <div class="total-row q-mt-lg">
            <div class="row items-center justify-between">
              <div class="text-subtitle1 text-weight-medium">مبلغ نهایی:</div>
              <div class="text-h6 text-weight-bold  text-primary text-weight-medium">
                {{ formatNumber(props.data.totalAmount) }}
                <span class="text-caption q-ml-sm">تومان</span>
              </div>
            </div>
          </div>
        </div>

      </q-card-section>

      <!-- Actions -->
      <q-card-actions align="right" class="action-section q-pa-md">
        <q-btn
          flat
          label="انصراف"
          color="grey-7"
          v-close-popup
          class="q-mr-sm"
          @click="resetCountDown"
        />
        <q-btn
          unelevated
          label=" ثبت سفارش"
          color="secondary"
          @click="submitOrder"
          :loading="loading"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { api } from "src/boot/axios";
import { ref, watchEffect } from "vue";
import { useQuasar } from "quasar";
import { useRouter } from "vue-router";

const show = ref(false);
const countdown = ref(85);
const loading = ref(false);
const fee = ref(10);
const $q = useQuasar();
const router = useRouter()

const props = defineProps(["data",'start']);



const formatNumber = (num) => {
  return new Intl.NumberFormat("fa-IR").format(num);
};

let countdownInterval;

const startCountdown = () => {
  countdownInterval = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--;
    } else {
      clearInterval(countdownInterval);
      show.value = false;
    }
  }, 1000);
};

watchEffect(() => {
  if (props.start) {
    startCountdown();
  }
});


const submitOrder = async () => {
  if (props.data.amountInGrams && countdown.value) {
    loading.value = true;
    try {
      const response = await api.post("/gold-sell", {
        final_price: (props.data.totalAmount * 10).toString(),
        gold_amount: props.data.amountInGrams.toString(),
        current_price: (props.data.currentPrice * 10).toString(),
        goldis_fee: (props.data.calculateFee * 10).toString(),
      });

      console.log("Response:", response);

      if (response.status === 200 && response.data.success === true) {
        $q.notify({
          type: "positive",
          message: "عملیات با موفقیت انجام شد",
          position: "top-right",
        });
        router.push('/dashboard/Walletmessage');
      } else {
        $q.notify({
          message: "عملیات ناموفق لطفا مجدد تلاش کنید",
          type: "warning",
          position: "top-right",
        });
      }
    } catch (error) {
      console.error("Error in API request:", error);

      $q.notify({
        type: "negative",
        message: error.response?.data?.message || "عملیات ناموفق لطفا مجدد تلاش کنید",
        position: "top-right",
      });
    } finally {
      loading.value = false;
    }
  } else {
    $q.notify({
      type: "warning",
      message: "پیش فاکتور منقضی شد",
      position: 'top-right',
    });
    setTimeout(() => {
      window.location.reload();
    }, 800);
  }
};
const resetCountDown = () => {
  window.location.reload()
  if (countdownInterval) {
    clearInterval(countdownInterval);
    countdown.value = 85
    startCountdown()
  }
}

defineExpose({
  show
});



</script>

<style scoped>
.modern-payment-card {
  width: 100%;
  max-width: 480px;
  border-radius: 16px;
}

.gradient-header {
  background: linear-gradient(135deg, var(--q-primary) 100%, #2c5282 100%);
  border-radius: 16px 16px 0 0;
}

.content-section {
  padding: 24px;
}

.timer-banner {
  background-color: #fff3cd;
  border-bottom: 1px solid #ffeeba;
}

.price-summary-card {
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.details-card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.detail-row {
  border-bottom: 1px solid #e2e8f0;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  color: #64748b;
  font-size: 0.95rem;
}

.detail-value {
  display: flex;
  align-items: center;
}

.detail-value .amount {
  font-weight: 500;
  font-size: 1.1rem;
}

.detail-value .unit {
  color: #64748b;
  margin-right: 4px;
  font-size: 0.9rem;
}

.unit-badge {
  background: #f1f5f9;
  color: #64748b;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
}

.total-row {
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.payment-method-card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.action-section {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-radius: 0 0 16px 16px;
}

:deep(.q-btn) {
  border-radius: 8px;
  padding: 8px 24px;
}

/* Custom transitions */
:deep(.q-dialog__inner) {
  backdrop-filter: blur(4px);
}

:deep(.q-dialog__inner--minimized > div) {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
