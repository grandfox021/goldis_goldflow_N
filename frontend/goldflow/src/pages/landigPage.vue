<template>
  <q-page class="landing-page">
    <!-- Hero Section with Animated Background -->
    <div class="hero-section q-pa-md">
      <!-- Main container with gradient overlay -->
      <div class="main-container">
        <!-- Primary Card with Gold Effect Border -->
        <q-card class="main-card q-pa-xl">
          <!-- Animated Header Section -->
          <div class="header-content q-mb-xl">
            <div class="text-center">
              <!-- Brand name with shimmer effect -->
              <h1 class="brand-title text-h2 q-mb-xl shimmer-text">گلدیس</h1>
              <div class="text-h6 text-info text-weight-medium q-mb-lg">
                سامانه قانونی و امن خرید و فروش طلای آینده
              </div>
              <!-- Enhanced feature description -->
              <div class="feature-text q-mb-lg">
                خرید، فروش و پس انداز آنلاین و ۲۴ ساعته طلای آینده، صندوق طلای
                اختصاصی
              </div>
              <div class="security-text">
                نگهداری طلا در بانک های معتبر با ضمانت بانک مرکزی
              </div>
            </div>
          </div>

          <!-- Premium CTA Button -->
          <div class="cta-section text-center q-mb-xl">
            <q-btn
              class="premium-btn"
              unelevated
              size="large"
              label="خرید طلای آبشده"
              @click="router.push('/dashboard')"
            />
          </div>
        </q-card>

        <!-- Enhanced Stats Grid -->
        <div class="stats-grid row q-col-gutter-md q-mt-lg q-px-md">
          <div class="col-6 col-sm-6 col-md-3">
            <q-card class="stats-card">
              <q-card-section class="text-center q-pa-sm">
                <q-icon name="business" size="40px" color="primary" />
                <div class="text-h5 q-my-sm">۱۱ واحد</div>
                <div class="text-subtitle1">شعب تحویل طلا</div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-6 col-sm-6 col-md-3">
            <q-card class="stats-card">
              <q-card-section class="text-center q-pa-sm">
                <q-icon name="people" size="40px" color="primary" />
                <div class="text-h5 q-my-sm">۵۰۰,۰۰۰+</div>
                <div class="text-subtitle1">کاربر فعال</div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-6 col-sm-6 col-md-3">
            <q-card class="stats-card">
              <q-card-section class="text-center q-pa-sm">
                <q-icon name="diamond" size="40px" color="primary" />
                <div class="text-h5 q-my-sm">۵۷+ کیلوگرم</div>
                <div class="text-subtitle1">پشتوانه طلای بانکی</div>
              </q-card-section>
            </q-card>
          </div>

          <div class="col-6 col-sm-6 col-md-3">
            <q-card class="stats-card">
              <q-card-section class="text-center q-pa-sm">
                <q-icon name="payments" size="40px" color="primary" />
                <div class="text-h5 q-my-sm">نیم درصد</div>
                <div class="text-subtitle1">کارمزد خرید و فروش</div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
    </div>
    <calculateComponent />
    <carusellComponent />
  </q-page>
</template>

<script setup>
import { defineAsyncComponent } from "vue";
import { useRouter } from "vue-router";

const calculateComponent = defineAsyncComponent(() => import('../components/mainLayout/calculateComponent.vue'))
const carusellComponent = defineAsyncComponent(() => import('../components/mainLayout/carouselComponent.vue'))
const router = useRouter()
</script>

<style lang="scss" scoped>
.landing-page {
  background: var(--q-info);
  min-height: 100vh;
}

.hero-section {
  position: relative;
  overflow: hidden;
  margin-bottom: 100px;
  margin-top: 40px;

  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("/images/pattern.png") repeat;
    opacity: 0.1;
    animation: shimmerBackground 15s linear infinite;
  }
}

.main-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  z-index: 1;
}

.main-card {
  background: linear-gradient(
    135deg,
    var(--q-primary) 0%,
    var(--q-primary) 100%
  );
  backdrop-filter: blur(10px);
  border: 1px solid var(--q-info);
  border-radius: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  overflow: hidden;

  &::before {
    content: "";
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(
      45deg,
      var(--q-primary),
      transparent,
      var(--q-info)
    );
    z-index: -1;
    animation: borderGlow 3s linear infinite;
  }
}

.brand-title {
  background: linear-gradient(
    to right,
    #ffffff 20%,
    var(--q-primary) 40%,
    var(--q-primary) 60%,
    #ffffff 80%
  );
  background-size: 200% auto;
  color: #000;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s linear infinite;
}

.premium-btn {
  background: linear-gradient(
    135deg,
    var(--q-secondary) 50%,
    var(--q-info) 100%
  );
  color: #000;
  font-weight: bold;
  padding: 12px 36px;
  border-radius: 12px;
  font-size: 1.2rem;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;

  &::before {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: rgba(255, 255, 255, 0.2);
    transform: rotate(45deg);
    animation: buttonShine 3s linear infinite;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3);
  }
}

.stats-card {
  background: var(--q-info);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    background: var(--q-info);
  }

  .q-icon {
    transition: transform 0.3s ease;
  }

  &:hover .q-icon {
    transform: scale(1.1);
  }
}

@keyframes shine {
  to {
    background-position: 200% center;
  }
}

@keyframes buttonShine {
  from {
    transform: rotate(45deg) translate(-100%, -100%);
  }
  to {
    transform: rotate(45deg) translate(100%, 100%);
  }
}

@keyframes borderGlow {
  0%,
  100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

@keyframes shimmerBackground {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 100% 100%;
  }
}

.feature-text,
.security-text {
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.9);
}

.stats-grid {
  margin-top: -50px;
}
</style>
