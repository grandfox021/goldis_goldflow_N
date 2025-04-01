<template>
  <q-dialog persistent>
    <q-card class="guide-dialog">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6 q-ml-auto">راهنمای فروش</div>
        <q-btn
          v-close-popup
          flat
          round
          icon="close"
          color="grey-7"
          class="q-ml-none"
        />
      </q-card-section>

      <q-card-section class="q-pt-lg">
        <!-- Guide Image -->
        <div class="text-center q-mb-lg">
          <img
            src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDAsIDQwKSI+CiAgICA8cGF0aCBkPSJNNjAgMEwxMjAgNjBMNjAgMTIwTDAgNjBMNjAgMFoiIGZpbGw9IiNGRkQ3MDAiLz4KICAgIDxwYXRoIGQ9Ik02MCAyMEw5MCA2MEw2MCAxMDBMMzAgNjBMNjAgMjBaIiBmaWxsPSIjRkZGRkZGIi8+CiAgPC9nPgo8L3N2Zz4K"
            alt="راهنمای فروش"
            style="width: 120px; height: 120px"
          />
        </div>

        <!-- Guide Content -->
        <div class="text-primary text-weight-medium q-mb-md">راهنمای فروش</div>

        <div class="guide-items q-gutter-y-md">
          <div class="guide-item">
            ۱- قیمت لحظه‌ای طلا در هنگام خرید و فروش قابل مشاهده است.
          </div>

          <div class="guide-item">
            ۲- در هنگام فروش پیش فاکتور صادر شده تا ۵ ثانیه شامل تغییر قیمت
            لحظه‌ای نخواهد شد.
          </div>

          <div class="guide-item">
            ۳- پس از فروش، مبلغ آن به کیف تومانی شما منتقل خواهد شد و برای واریز
            به حساب بانکی باید به منوی امور مالی-بخش برداشت وجه مراجعه نموده و
            درخواست برداشت بانکی خود را ثبت کنید.
          </div>

          <div class="guide-item">
            ۴- شما می‌توانید تا سقف موجودی صندوق طلای خود عملیات فروش را انجام
            دهید.
          </div>

          <div class="guide-item">
            ۵- کارمزد ریالی فروش طلای آب‌شده به سامانه نیم درصد از حداقل ۱ سوت
            می‌باشد که از جمع فاکتور کسر می‌شود
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="center" class="q-pb-md">
        <q-btn
          unelevated
          color="dark"
          class="full-width"
          style="max-width: 200px"
          label="متوجه شدم"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup></script>

<style scoped>
.guide-dialog {
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
}

.guide-items {
  font-size: 14px;
  line-height: 1.6;
  color: #424242;
}

.guide-item {
  position: relative;
  padding-right: 8px;
}

.guide-item::before {
  content: "";
  position: absolute;
  right: 0;
  top: 10px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: var(--q-primary);
  display: none; /* Since numbers are used instead of bullets */
}
</style>
