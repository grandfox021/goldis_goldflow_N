<template>
  <div class="withdrawal-container q-pa-md ">
    <h4 class="text-h5 q-mb-md text-weight-medium">درخواست‌های برداشت</h4>

    <div class="withdrawal-list">
      <q-card
        v-for="request in withdrawalRequests"
        :key="request.id"
        class="withdrawal-card q-mb-md"
        :class="`status-${request.status}`"
        flat
        bordered
      >
        <!-- Status and Amount Area -->
        <div class="row items-center withdrawal-header">
          <div class="col-12 col-sm-6">
            <div class="text-h5 text-weight-bold amount-display">
              {{ request.amount.toLocaleString() }}
              <span class="currency">تومان</span>
            </div>
            <div class="text-caption text-grey-8 q-mt-xs">
              شناسه: {{ request.id }}
            </div>
          </div>
          <div class="col-12 col-sm-6 text-right text-sm-right">
            <q-badge
              :color="getStatusColor(request.status)"
              :text-color="getStatusTextColor(request.status)"
              class="status-badge q-px-md q-py-sm"
            >
              {{ getStatusText(request.status) }}
            </q-badge>
          </div>
        </div>

        <q-separator class="q-my-md" />

        <!-- Details Area -->
        <div class="row q-col-gutter-md details-area">
          <div class="col-12 col-sm-6">
            <div class="detail-block">
              <div class="detail-label">شماره کارت</div>
              <div class="detail-value">
                <div class="card-number">
                  <span dir="ltr">{{ formatCardNumber(request.cardNumber) }}</span>
                  <q-btn
                    flat
                    dense
                    round
                    icon="content_copy"
                    size="xs"
                    class="copy-btn q-ml-md"
                    @click="copyToClipboard(request.cardNumber)"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-sm-6">
            <div class="detail-block">
              <div class="detail-label">تاریخ و زمان</div>
              <div class="detail-value">
                <div class="date-time">
                  {{ request.date }} - {{ request.time }}
                </div>
              </div>
            </div>
          </div>
        </div>

      </q-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useQuasar } from 'quasar';
import { api } from 'src/boot/axios';
const q = useQuasar();

const userId = localStorage.getItem('userId')



const getStatusText = status => {
  switch (status) {
    case 'completed': return 'تایید شده';
    case 'pending': return 'در انتظار بررسی';
    case 'rejected': return 'رد شده';
    case 'canceled': return 'لغو شده';
    default: return 'نامشخص';
  }
};

const getStatusColor = status => {
  switch (status) {
    case 'completed': return 'green-2';
    case 'pending': return 'amber-2';
    case 'rejected': return 'red-2';
    case 'canceled': return 'grey-4';
    default: return 'grey-4';
  }
};

const getStatusTextColor = status => {
  switch (status) {
    case 'completed': return 'green-10';
    case 'pending': return 'amber-10';
    case 'rejected': return 'red-10';
    case 'canceled': return 'grey-10';
    default: return 'grey-10';
  }
};

const formatCardNumber = (cardNumber) => {
  return cardNumber.replace(/(\d{4})/g, '$1 ').trim();
};



const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    q.notify({
      message: 'شماره کارت کپی شد',
      color: 'positive',
      position: 'top-right',
      timeout: 1500,
      icon: 'check_circle'
    });
  });
};
const withdrawalRequests = ref([
  { id: 1, date: '1404/05/12', time: '10:28:32', amount: 500000, cardNumber: '6219861034529871', status: 'approved' },
  { id: 2, date: '1404/06/05', time: '18:42:15', amount: 750000, cardNumber: '6037997212345678', status: 'pending' },
  { id: 3, date: '1404/06/09', time: '09:15:20', amount: 300000, cardNumber: '6219861034529871', status: 'rejected' },
  { id: 4, date: '1404/06/18', time: '14:25:44', amount: 1000000, cardNumber: '6037997212345678', status: 'canceled' }
]);

const fetchTarakoneshData = async() => {
  const { data } = await api.get(`/get-withdrawl-requests-for-user/${userId}`)
  const newTarakonesh = data.withdrawal_requests.map(item => ({
    id: item.id,
    date: item.created_at,
    amount : item.amount,
    cardNumber: item.card_number,
    status: item.status
  }))
  withdrawalRequests.value = newTarakonesh
}

onMounted(fetchTarakoneshData)
</script>

<style scoped>
.withdrawal-card {
  border-radius: 12px;
  padding: 16px;
  transition: all 0.2s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.withdrawal-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.withdrawal-header {
  padding-bottom: 10px;
}

.amount-display {
  font-size: 1.5rem;
  color: #333;
}

.currency {
  font-size: 0.9rem;
  margin-right: 4px;
  color: #666;
}

.status-badge {
  border-radius: 30px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.details-area {
  margin: 12px 0;
}

.detail-block {
  margin-bottom: 12px;
}

.detail-label {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 4px;
}

.detail-value {
  font-size: 0.95rem;
  font-weight: 500;
  color: #333;
}

.card-number {
  display: flex;
  align-items: center;
  letter-spacing: 0.5px;
}

.bank-name {
  margin-top: 2px;
}

.date-time {
  display: flex;
  align-items: center;
}

.copy-btn {
  opacity: 0.6;
  margin-right: 8px;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  opacity: 1;
}

.action-area {
  margin-top: 12px;
}

@media (max-width: 600px) {
  .withdrawal-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .status-badge {
    margin-top: 8px;
  }

  .amount-display {
    font-size: 1.25rem;
  }
}

/* Status styles with gradients */
.status-completed {
  border-left: 4px solid #21BA45;
}

.status-pending {
  border-left: 4px solid #F2C037;
}

.status-rejected {
  border-left: 4px solid #C10015;
}

.status-canceled {
  border-left: 4px solid #616161;
}
</style>
