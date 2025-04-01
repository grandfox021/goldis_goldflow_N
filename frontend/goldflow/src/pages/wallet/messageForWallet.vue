<template>
  <q-page class="row justify-center">
    <q-card class="success-card q-pa-lg" flat bordered>
      <div  class="text-center success-content">
        <div  class="checkmark-container q-mb-md">
          <q-icon name="check" color="primary" size="4rem" class="checkmark-icon" />
          <div class="checkmark-pulse"></div>
        </div>
        <div class="text-h5 text-center text-weight-bold q-mb-sm q-mt-md text-primary">پیام سیستم</div>
        <div class="text-body1 q-mb-lg text-secondary">
          عملیات با موفقیت انجام شد ، در حال انتقال ...
        </div>
        <q-btn
          unelevated
          rounded
          color="primary"
          class="continue-btn q-px-md q-py-sm"
          :ripple="false"
          label="بازگشت به داشبورد"
        />
      </div>
    </q-card>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
onMounted(() => {
  setTimeout(() => {
    router.push('/dashboard/reciept')
  }, 2000);
})
</script>

<style scoped>

.success-card {
  width: 100%;
  border-radius: 16px;
  border-color: rgba(224, 242, 241, 0.6);
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(240, 253, 250, 0.9));
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
}

.success-card:hover {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.success-content {
  opacity: 1;
  transform: translateY(10px);
  transition: all 0.5s ease;
}

.checkmark-container {
  background: linear-gradient(145deg, #ffffff, #f0fdfa);
  width: 90px;
  height: 90px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
  box-shadow: 0 6px 15px rgba(38, 166, 154, 0.15);
  z-index: 1;
}

.checkmark-icon {
  margin-bottom: 6px;
  opacity: 0.95;
  transform: scale(0.8);
  transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 2;
}

.checkmark-icon.scale-up {
  transform: scale(1);
}

.checkmark-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: rgba(38, 166, 154, 0.1);
  z-index: 0;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.3;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.7;
  }
}

.primary-text {
  color: #1a1a1a;
  font-family: 'Vazir', 'Tahoma', Arial, sans-serif;
  letter-spacing: -0.2px;
}

.secondary-text {
  color: #555555;
  font-family: 'Vazir', 'Tahoma', Arial, sans-serif;
  line-height: 1.5;
  font-size: 1rem;
}

.continue-btn {
  font-family: 'Vazir', 'Tahoma', Arial, sans-serif;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.continue-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(38, 166, 154, 0.2);
}

.continue-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transition: all 0.7s ease;
}

.continue-btn:hover::before {
  left: 100%;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .success-card {
    background: linear-gradient(145deg, rgba(38, 50, 56, 0.9), rgba(25, 35, 40, 0.9));
    border-color: rgba(55, 71, 79, 0.6);
  }

  .checkmark-container {
    background: linear-gradient(145deg, #37474f, #263238);
  }

  .primary-text {
    color: #e0e0e0;
  }

  .secondary-text {
    color: #b0bec5;
  }

  .checkmark-pulse {
    background-color: rgba(38, 166, 154, 0.2);
  }
}
</style>
