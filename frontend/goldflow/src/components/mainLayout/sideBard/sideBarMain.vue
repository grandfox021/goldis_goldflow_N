<template>
  <div>
    <!-- Desktop Navigation -->
    <div class="row q-gutter-x-md gt-sm nav-links">
              <q-btn
                v-for="(item, index) in navigationItems"
                :key="index"
                flat
                :label="item.label"
                :to="item.route"
                class="nav-link text-accent"
                no-caps
              />
            </div>
  </div>
</template>

<script setup>
const navigationItems = [
  { label: "خانه", route: "/" },
  { label: "درباره ما", route: "/about" },
  { label: "تماس با ما", route: "/contact" },
  { label: "مجله", route: "/blog" },
];
</script>

<style scoped>
/* Navigation Links */
.nav-links {
  margin-right: 24px;
}

.nav-link {
  position: relative;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-link::after {
  content: "";
  position: absolute;
  bottom: 4px;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: var(--q-primary);
  transition: all 0.3s ease;
  transform: translateX(-50%);
  opacity: 0;
}

.nav-link:hover {
  background: rgba(var(--q-primary-rgb), 0.05);
}

.nav-link:hover::after {
  width: calc(100% - 32px);
  opacity: 1;
}
</style>
