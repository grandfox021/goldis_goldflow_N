<template>
  <q-page class="q-pa-md">
    <!-- Card Registration Section -->
    <div class="modern-card q-pa-lg q-mb-lg">
      <div class="text-center">
        <q-icon name="credit_card" size="md" color="primary" />
        <div class="text-h5 q-mb-md text-primary">ثبت کارت</div>
      </div>

      <q-separator></q-separator>

      <!-- Rules Section -->
      <div class="rules-container q-pa-md q-mb-lg">
        <q-list class="rounded-borders">
          <q-item v-for="(rule, index) in rules" :key="index">
            <q-item-section avatar>
              <q-icon name="info" color="primary" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-accent">{{ rule }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </div>

      <!-- Card Input Section -->

      <q-form @submit.prevent="registerCard">
      <div class="row q-gutter-md justify-center">
          <div class="col-12 col-md-5">
          <q-input
            v-model="cardNumber"
            v-persian-numbers
            placeholder="شماره کارت را وارد کنید"
            outlined
            class="card-input flex flex-center"
            :rules="[
              (val) =>
                val.length === 16 || 'لطفا شماره کارت 16 رقمی را وارد کنید',
            ]"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon
                name="credit_card"
                color="primary"
                class="flex flex-center q-pl-sm"
              />
            </template>
            <template v-slot:append v-if="cardNumber">
              <q-icon
                name="close"
                class="cursor-pointer"
                @click="cardNumber = ''"
              />
            </template>
          </q-input>
        </div>
        <div class="col-12 col-md-3 text-center">
          <q-btn
            unelevated
            color="primary"
            class="full-width submit-button"
            :loading="isSubmitting"
            type="submit"
          >
            <span class="text-weight-bold">ثبت کارت</span>
            <template v-slot:loading>
              <q-spinner-dots />
            </template>
          </q-btn>
        </div>

      </div>
    </q-form>
    </div>

    <!-- Cards List Section -->
    <div class="modern-card q-pa-lg">
      <div class="flex items-center justify-center q-mb-lg">
        <div class="text-h5 text-primary flex items-center">
          کارت‌های ثبت شده
        </div>
      </div>
      <q-separator class="q-mb-lg"></q-separator>

      <div v-if="cards.length === 0" class="text-center q-pa-lg">
        <q-icon name="credit_card_off" size="4em" color="grey-5" />
        <div class="text-h6 text-grey-7 q-mt-md">هیچ کارتی ثبت نشده است</div>
      </div>

      <div v-else class="row q-col-gutter-md">
        <div v-for="card in cards" :key="card.id" class="col-12 col-md-4">
          <q-card class="card-item">
            <q-card-section>
              <div class="row items-center justify-between">
                <div class="flex items-center">
                  <div class="text-weight-bold">{{ card.label }}</div>
                </div>
                <div>
                  <q-btn
                    flat
                    round
                    class="bg-info q-ml-xs"
                    color="primary"
                    size="sm"
                    icon="edit"
                    @click="editCard(card)"
                  />
                  <q-btn
                    flat
                    round
                    class="bg-info"
                    color="negative"
                    size="sm"
                    icon="delete"
                    @click="confirmDelete(card)"
                  />
                </div>
              </div>
            </q-card-section>

            <q-card-section>
              <div class="card-number-display q-pa-sm">
                <div dir="ltr" class="text-weight-medium">
                  {{ formatCardNumber(card.cardNumber) }}
                </div>
                <q-btn
                  flat
                  round
                  size="sm"
                  icon="content_copy"
                  @click="copyToClipboard(card.cardNumber)"
                />
              </div>
            </q-card-section>

            <q-card-section>
              <q-btn
                :color="card.status === 'verified' ? 'primary' : 'secondary'"
                :label="
                  card.status === 'verified' ? 'تایید شده' : 'در انتظار تایید'
                "
                class="full-width"
                :icon="card.status === 'verified' ? 'check_circle' : 'pending'"
                dir="rtl"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import { api } from "src/boot/axios";
import { persianToEnglish } from "src/composable/useNumberUtils";

const $q = useQuasar();
const cardNumber = ref("");
const isSubmitting = ref(false);
const cardStatus = ref("verified");

const rules = [
  "کارت بانکی باید متعلق به خود شما باشد.",
  "خرید با افزایش اعتبار از طریق درگاه بانکی فقط با شماره کارت ثبت شده امکان پذیر است.",
  "در صورتی که با کارت ثبت نشده خرید با افزایش اعتبار نمایید، وجه طی ۲۴ الی ۷۲ ساعت کاری به حساب شما برگشت می شود.",
];

const cards = ref([]);

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


const formatCardNumber = (number) => {
  return number.replace(/(\d{4})/g, "$1 ").trim();
};

const registerCard = async () => {
  if (cardNumber.value.length !== 16) {
    $q.notify({
      type: "warning",
      message: "لطفا شماره کارت معتبر وارد کنید",
      position: "top-right",
    });
    return;
  }

  isSubmitting.value = true;
  try {
    const { data } = await api.post("/post-card-number", {
      card_number: persianToEnglish((cardNumber.value).toString()),
    });
    fetchCardsData()
    console.log(data);
    $q.notify({
      type: "positive",
      message: "کارت با موفقیت ثبت شد",
      position: "top-right",
    });
    cardNumber.value = "";
  } catch (error) {
    console.log(error);
    $q.notify({
      type: "negative",
      message: "خطا در ثبت کارت",
      position: "top-right",
    });
  } finally {
    isSubmitting.value = false;
    cardNumber.value = "";
  }
};

const fetchCardsData = async() => {
  const { data } = await api.get('/get-card-number')
  const cleanCard = data.card_number.toString()
  const bin = cleanCard.substring(0,6)
  const bankLabel = bankBins[bin] || 'نامشخص'
 console.log(data.card_number);
  const newCard = {
    label : bankLabel,
    cardNumber: data.card_number,
    cardStatus : cardStatus.value
  }
  cards.value.unshift(newCard)
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
  $q.notify({
    type: "positive",
    message: "شماره کارت کپی شد",
    position: "top-right",
  });
};

const confirmDelete = (card) => {
  $q.dialog({
    title: "حذف کارت",
    message: "آیا از حذف این کارت اطمینان دارید؟",
    cancel: true,
    persistent: true,
  }).onOk(async() => {
    // Handle delete
    const { data } = await api.delete("/delete-card-number");
    console.log(data);
    cards.value = cards.value.filter((c) => c.id !== card.id);
    $q.notify({
      type: "positive",
      message: "کارت با موفقیت حذف شد",
      position: "top-right",
    });
  });
};

const editCard = (card) => {
  console.log(card);
  // Handle edit
};


onMounted(fetchCardsData)
</script>

<style scoped>
.modern-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid var(--q-info);
}

.card-input :deep(.q-field__control) {
  height: 56px;
  border-radius: 12px;
}

.card-input :deep(.q-field__control:before) {
  border: 2px solid #e0e0e0;
}

.card-input :deep(.q-field__control:hover:before) {
  border-color: var(--q-primary);
}

.submit-button {
  height: 56px;
  border-radius: 12px;
  font-weight: 500;
  transition: transform 0.2s;
}

.submit-button:hover {
  transform: translateY(-2px);
}

.card-item {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.card-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.card-number-display {
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rules-container {
  border-radius: 12px;
}

/* RTL Support */
:deep(.q-field__control) {
  direction: rtl;
}

:deep(.q-item) {
  direction: rtl;
}
</style>
