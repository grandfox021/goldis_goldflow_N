<template>
   <div class="bg-info custom-padding">
    <q-footer class="footer-container q-mx-auto q-pa-lg">

      <div class="q-pa-xl">
        <!-- Main Content Grid -->
        <div class="row q-col-gutter-xl">
          <!-- Navigation Links -->
          <div class="col-6 col-md-3">
            <h6 class="text-info q-mb-md footer-heading">دسترسی سریع</h6>
            <q-list class="nav-list">
              <q-item
                v-for="link in navLinks"
                :key="link.title"
                clickable
                v-ripple
                :to="link.route"
                class="nav-link"
              >
                <q-item-section>
                  <div class="row items-center justify-start q-px-sm">
                    <q-icon
                      :name="link.icon"
                      size="xs"
                      class="q-mr-sm text-secondary"
                    />
                    <span class="text-info">{{ link.title }}</span>
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </div>

          <!-- Contact Info -->
          <div class="col-6 col-md-3">
            <h6 class="text-info q-mb-md footer-heading">اطلاعات تماس</h6>
            <div class="contact-items">
              <div class="contact-item row items-center q-mb-md">
                <div class="contact-text flex">
                  <div class="flex row item">
                    <q-icon name="location_on" size="sm" class="q-mr-sm text-secondary" />
                     <div>تهران، خیابان طرشت</div>
                  </div>
                  <div class="text-caption text-grey-5">
                    ساختمان گلدیس، طبقه ۲
                  </div>
                </div>
              </div>

              <a
                href="tel:+98996633219"
                class="contact-item row items-center q-mb-md"
              >
                <q-icon name="phone" size="sm" class="q-mr-sm text-secondary" />
                <div class="contact-text">98996633219+</div>
              </a>

              <a
                href="mailto:info@goldis.ir"
                class="contact-item row items-center"
              >
                <q-icon name="email" size="sm" class="q-mr-sm  text-secondary" />
                <div class="contact-text">info@goldis.ir</div>
              </a>
            </div>
          </div>

          <!-- About Section -->
          <div class="col-12 col-md-5">
            <h6 class="text-info q-mb-md footer-heading">درباره گلدیس</h6>
            <p class="text-info q-mb-lg about-text">
              گلدیس در راستای تسهیل فرایند خرید طلا با تکیه بر دانش فنی و تیم
              متخصص امکان مقایسه، بررسی و مشاهدی قیمت لحظه ای طلا در هر ساعتی از
              شبانه روز و امکان خرید لحظه ای و دریافت طلای آینده را فراهم آورده.
            </p>

            <!-- Social Media Icons -->
            <div class="social-icons q-mt-md">
              <q-btn
                flat
                round
                color="info"
                icon="telegram"
                class="q-mr-sm social-btn"
              />
              <q-btn
                flat
                round
                color="info"
                icon="mdi-instagram"
                class="q-mr-sm social-btn"
              />
              <q-btn
                flat
                round
                color="info"
                icon="mdi-linkedin"
                class="q-mr-sm social-btn"
              />
              <q-btn
                flat
                round
                color="info"
                icon="mdi-twitter"
                class="social-btn"
              />
            </div>
          </div>
        </div>


      </div>

      <!-- Back to Top Button -->
      <q-page-sticky position="bottom-left" :offset="[20, 20]">
        <q-btn
          v-show="showBackToTop"
          round
          color="primary"
          icon="keyboard_arrow_up"
          class="back-to-top-btn"
          @click="scrollToTop"
        />
      </q-page-sticky>
    </q-footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const showBackToTop = ref(false);

const navLinks = [
  { title: "خانه", icon: "home", route: "/" },
  { title: "خدمات", icon: "shopping_bag", route: "/services" },
  { title: "درباره ما", icon: "info", route: "/about" },
  { title: "قوانین", icon: "gavel", route: "/terms" },
];

const handleScroll = () => {
  showBackToTop.value = window.pageYOffset > 300;
};

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style lang="scss">
.footer-container {
  position: relative;
  overflow: hidden;
  max-width: 1400px;
  border-top-left-radius: 25px;
  border-top-right-radius: 25px;

  // Modern gradient background
  .gradient-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--q-primary);
    opacity: 0.97;
    z-index: -1;
  }

  // Typography improvements
  .footer-heading {
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    position: relative;

    &:after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -8px;
      width: 40px;
      height: 2px;
      background: $secondary;
      transition: width 0.3s ease;
    }

    &:hover:after {
      width: 60px;
    }
  }

  // Enhanced navigation links
  .nav-list {
    .nav-link {
      padding: 8px 0;
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateX(-4px);

        .q-icon {
          transform: translateX(-4px);
          color: $primary;
        }
      }

      .q-icon {
        transition: all 0.3s ease;
      }
    }
  }

  // Contact items styling
  .contact-items {
    .contact-item {
      text-decoration: none;
      color: white;
      padding: 8px 0;
      transition: all 0.3s ease;

      &:hover {
        .contact-text {
          transform: translateX(-4px);
        }

        .q-icon {
          transform: scale(1.1);
        }
      }

      .contact-text {
        transition: transform 0.3s ease;
      }

      .q-icon {
        transition: transform 0.3s ease;
      }
    }
  }

  // About section
  .about-text {
    line-height: 1.8;
    color: $grey-5;
  }

  // Social media buttons
  .social-icons {
    .social-btn {
      position: relative;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-4px);

        &:before {
          transform: scale(1.2);
          opacity: 0;
        }
      }

      &:before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: $info;
        border-radius: 50%;
        z-index: -1;
        transition: all 0.3s ease;
        opacity: 0.2;
      }
    }
  }

  // Newsletter section
  .newsletter-section {
    .subscribe-btn {
      border-radius: 0 4px 4px 0;
      height: 40px;
    }

    .q-input {
      .q-field__control {
        height: 40px;
        background: rgba(255, 255, 255, 0.05);
      }
    }
  }

  // Trust badges
  .trust-badge {
    transition: all 0.3s ease;
    opacity: 0.8;

    &:hover {
      opacity: 1;
      transform: translateY(-2px);
    }
  }

  // Back to top button
  .back-to-top-btn {
    opacity: 1;
    transform: translateY(20px);
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba($primary, 0.3);

    &.show {
      opacity: 1;
      transform: translateY(0);
    }

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 6px 20px rgba($primary, 0.4);
    }
  }

  // Responsive adjustments
  @media (max-width: $breakpoint-sm-max) {
    .newsletter-section {
      text-align: center;

      .text-right {
        text-align: center !important;
      }
    }

    .footer-heading{
      font-size: 1rem;
    }
    .footer-heading:after {
      right: 50%;
      transform: translateX(50%);
    }

    .nav-list,
    .contact-items,
    .about-text {
      text-align: left !important;
    }

    .social-icons {
      justify-content: center;
      display: flex;
    }

    .contact-item {
      min-width: 200px;
      justify-content: start;
    }
  }
}
.custom-padding{
  padding-top: 50px;
}
</style>
