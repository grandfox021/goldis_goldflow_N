<template>
  <div class="features-section q-py-xl">
    <div class="text-center q-mb-xl q-px-md">
      <div class="section-title text-h4 q-mb-md">امکانات گلدیس</div>
      <div class="section-subtitle text-subtitle1 q-mx-auto" style="max-width: 800px">
        گلدیس به عنوان یکی از بزرگترین مراکز معتبر خرید و فروش آنلاین طلای آینده
        در کشور، همواره می‌کوشد امکانات و مزایای ویژه و متفاوتی را به مشتریان
        خود ارائه دهد
      </div>
    </div>

    <div class="features-slider-container">
      <q-btn
        round
        flat
        color="primary"
        icon="chevron_right"
        class="slider-arrow left-arrow"
        @click="previousSlide"
        :class="{ 'mobile-hidden': isMobile }"
      />
      <div class="slider-wrapper">
        <div class="slider-track" ref="sliderTrack" @touchstart="handleTouchStart" @touchmove="handleTouchMove" @touchend="handleTouchEnd">
          <div v-for="(feature, index) in duplicatedFeatures" :key="index" class="slide">
            <div class="feature-card">
              <div class="icon-wrapper">
                <q-icon :name="feature.icon" size="48px" color="primary" />
              </div>
              <div class="text-h5 text-accent text-center q-mt-md text-weight-bold">
                {{ feature.title }}
              </div>
              <p class="text-subtitle2 q-mt-sm text-center">
                {{ feature.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
      <q-btn
        round
        flat
        color="primary"
        icon="chevron_left"
        class="slider-arrow right-arrow"
        @click="nextSlide"
        :class="{ 'mobile-hidden': isMobile }"
      />
    </div>

    <!-- Mobile indicators -->
    <div v-if="isMobile" class="mobile-indicators q-mt-md">
      <div
        v-for="(feature, index) in features"
        :key="`indicator-${index}`"
        class="indicator"
        :class="{ 'active': currentSlideIndex === index }"
        @click="goToSlide(index)"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useQuasar } from "quasar";

const $q = useQuasar();
const isMobile = ref(false);

const features = ref([
  { id: 1, icon: "phone", title: "پشتیبانی ۲۴ ساعته", description: "پشتیبانی ۲۴ ساعته حتی در روزهای تعطیل" },
  { id: 2, icon: "verified", title: "اعتبار و اصالت", description: "عضو گروه مالی پیشرو ملی با ۵ سال سابقه" },
  { id: 3, icon: "security", title: "امنیت زیرساخت", description: "استفاده از متد‌های امنیتی هوش مصنوعی" },
  { id: 4, icon: "speed", title: "سرعت معاملات", description: "بالاترین سرعت انجام معاملات آنلاین" },
  { id: 5, icon: "price_check", title: "قیمت‌های رقابتی", description: "بهترین قیمت‌ها با کمترین کارمزد" },
]);

// Duplicate slides for seamless looping
const duplicatedFeatures = computed(() => [...features.value, ...features.value]);

const sliderTrack = ref(null);
let animationFrame;
let position = 0;
const speed = ref(0.3); // Adjust speed dynamically based on device
let slideWidth = ref(300); // Will be updated based on viewport
const currentSlideIndex = ref(0);

// Touch handling for mobile swipes
let touchStartX = 0;
let touchEndX = 0;

const handleTouchStart = (e) => {
  if (isMobile.value) {
    stopAutoScroll();
    touchStartX = e.touches[0].clientX;
  }
};

const handleTouchMove = (e) => {
  if (isMobile.value) {
    touchEndX = e.touches[0].clientX;
    const diff = touchStartX - touchEndX;

    // Add resistance to prevent overscroll
    const resistance = 0.3;
    sliderTrack.value.style.transform = `translateX(${position - (diff * resistance)}px)`;
  }
};

const handleTouchEnd = () => {
  if (isMobile.value) {
    const diff = touchStartX - touchEndX;

    // If swiped far enough, change slide
    if (Math.abs(diff) > 50) {
      if (diff > 0) {
        nextSlide();
      } else {
        previousSlide();
      }
    } else {
      // Return to original position if swipe wasn't far enough
      sliderTrack.value.style.transition = "transform 0.3s ease-out";
      sliderTrack.value.style.transform = `translateX(${position}px)`;
      setTimeout(() => {
        sliderTrack.value.style.transition = "none";
        startAutoScroll();
      }, 300);
    }
  }
};

const calculateSlideWidth = () => {
  isMobile.value = $q.screen.width < 768;

  if (isMobile.value) {
    slideWidth.value = $q.screen.width * 0.8; // 80% of screen width on mobile
    speed.value = 0.15; // Slower speed on mobile
  } else {
    slideWidth.value = 300; // Default width on desktop
    speed.value = 0.3; // Normal speed on desktop
  }

  // Reset position after resize
  position = 0;
  sliderTrack.value.style.transform = `translateX(${position}px)`;
};

const animate = () => {
  position -= speed.value;
  sliderTrack.value.style.transform = `translateX(${position}px)`;

  // Update current slide index for indicators
  const adjustedPosition = Math.abs(position);
  currentSlideIndex.value = Math.floor(adjustedPosition / slideWidth.value) % features.value.length;

  if (Math.abs(position) >= sliderTrack.value.clientWidth / 2) {
    position = 0;
  }

  animationFrame = requestAnimationFrame(animate);
};

const startAutoScroll = () => {
  if (!isMobile.value) {
    animationFrame = requestAnimationFrame(animate);
  }
};

const stopAutoScroll = () => {
  cancelAnimationFrame(animationFrame);
};

// Move to next slide manually
const nextSlide = () => {
  stopAutoScroll();
  const slideMove = isMobile.value ? slideWidth.value : 320;
  position -= slideMove;
  sliderTrack.value.style.transition = "transform 0.5s ease-out";
  sliderTrack.value.style.transform = `translateX(${position}px)`;

  // Update current slide index for indicators
  currentSlideIndex.value = (currentSlideIndex.value + 1) % features.value.length;

  setTimeout(() => {
    sliderTrack.value.style.transition = "none"; // Reset transition for infinite effect
    if (Math.abs(position) >= sliderTrack.value.clientWidth / 2) {
      position = 0;
      sliderTrack.value.style.transform = `translateX(${position}px)`;
    }
    if (!isMobile.value) startAutoScroll();
  }, 500);
};

// Move to previous slide manually
const previousSlide = () => {
  stopAutoScroll();
  const slideMove = isMobile.value ? slideWidth.value : 320;
  position += slideMove;
  sliderTrack.value.style.transition = "transform 0.5s ease-out";
  sliderTrack.value.style.transform = `translateX(${position}px)`;

  // Update current slide index for indicators
  currentSlideIndex.value = (currentSlideIndex.value - 1 + features.value.length) % features.value.length;

  setTimeout(() => {
    sliderTrack.value.style.transition = "none"; // Reset transition for infinite effect
    if (position > 0) {
      position = -sliderTrack.value.clientWidth / 2;
      sliderTrack.value.style.transform = `translateX(${position}px)`;
    }
    if (!isMobile.value) startAutoScroll();
  }, 500);
};

// Go to specific slide (for indicators)
const goToSlide = (index) => {
  stopAutoScroll();
  const targetPos = -index * slideWidth.value;
  position = targetPos;
  currentSlideIndex.value = index;

  sliderTrack.value.style.transition = "transform 0.5s ease-out";
  sliderTrack.value.style.transform = `translateX(${position}px)`;

  setTimeout(() => {
    sliderTrack.value.style.transition = "none";
  }, 500);
};

// Setup window resize listener
let resizeObserver;

onMounted(() => {
  calculateSlideWidth();

  // Create resize observer
  resizeObserver = new ResizeObserver(() => {
    calculateSlideWidth();
  });

  // Observe document body
  resizeObserver.observe(document.body);

  startAutoScroll();
});

onUnmounted(() => {
  stopAutoScroll();
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>

<style lang="scss">
.features-section {
  background-color: #f5f5f5;
  direction: rtl;
  overflow: hidden;
  position: relative;
}

.section-title {
  color: var(--q-primary);
  position: relative;
  display: inline-block;
  font-size: 2rem;

  @media (max-width: 767px) {
    font-size: 1.5rem;
  }

  &::after {
    content: "";
    position: absolute;
    bottom: -10px;
    right: 50%;
    transform: translateX(50%);
    width: 80px;
    height: 3px;
    background-color: var(--q-secondary);

    @media (max-width: 767px) {
      width: 60px;
    }
  }
}

.section-subtitle {
  color: #424242;
  line-height: 1.8;

  @media (max-width: 767px) {
    font-size: 0.9rem;
    line-height: 1.6;
  }
}

.features-slider-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  overflow: hidden;
  position: relative;
}

.slider-wrapper {
  display: flex;
  overflow: hidden;
  width: 80%;

  @media (max-width: 767px) {
    width: 90%;
  }
}

.slider-track {
  display: flex;
  white-space: nowrap;
  will-change: transform;
}

.slide {
  flex: 0 0 auto;
  width: 300px; /* Default width - will be overridden for mobile */
  padding: 0 10px;

  @media (max-width: 767px) {
    width: 80vw;
  }
}

.feature-card {
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;

  @media (max-width: 767px) {
    padding: 1.5rem;
  }

  .icon-wrapper {
    width: 80px;
    height: 80px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(27, 94, 32, 0.1);
    border-radius: 50%;
    margin-bottom: 1rem;

    @media (max-width: 767px) {
      width: 60px;
      height: 60px;
    }
  }

  .text-h5 {
    color: var(--q-primary);

    @media (max-width: 767px) {
      font-size: 1.1rem;
    }
  }

  p {
    color: var(--q-accent);
    line-height: 1.8;

    @media (max-width: 767px) {
      font-size: 0.85rem;
      line-height: 1.6;
    }
  }
}

.slider-arrow {
  width: 48px;
  height: 48px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin: 0 2rem;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;

  &:hover {
    background: #f5f5f5;
  }

  .q-icon {
    font-size: 1.5rem;
  }

  @media (max-width: 991px) {
    margin: 0 1rem;
    width: 40px;
    height: 40px;
  }
}

.mobile-hidden {
  display: none;
}

.left-arrow {
  left: 0;
}

.right-arrow {
  right: 0;
}

.mobile-indicators {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 1rem;

  .indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #ccc;
    cursor: pointer;
    transition: all 0.3s ease;

    &.active {
      background-color: var(--q-primary);
      transform: scale(1.2);
    }
  }
}
</style>
