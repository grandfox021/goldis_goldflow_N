<template>
     <!-- Floating Support Button with Animation -->
     <q-page-sticky class="position-container" position="bottom-right" :offset="[18, 18]">
        <q-btn round color="positive" class="support-btn pulse-animation">
          <div class="support-icon-container">
            <q-icon name="support_agent" size="md" />
          </div>
          <q-tooltip anchor="center right" self="center left" :offset="[10, 0]">
            پشتیبانی
          </q-tooltip>
        </q-btn>
      </q-page-sticky>
</template>

<style scoped>
.position-container{
  z-index: 999999 !important;
}
.support-btn {
  width: 60px;
  height: 60px;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.4);
  transition: all 0.3s ease;
  z-index: 1000000 !important;
  &:hover {
    transform: scale(1.05);
  }
}

.support-icon-container {
  background-color: var(--q-positive);
  border-radius: 50%;
  padding: 5px;
}

.pulse-animation {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}
</style>
