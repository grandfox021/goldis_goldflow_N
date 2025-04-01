<template>
  <q-page class="dashboard-page q-py-md q-px-md q-md-pa-lg">
    <div class="page-header q-mb-md">
    </div>

    <!-- Summary Cards -->
    <div dir="rtl" class="row q-col-gutter-md q-mb-md">
      <div class="col-12 col-sm-6 col-md-3" v-for="(card, index) in statsCards" :key="index">
        <q-card class="stats-card">
          <q-card-section class="q-pa-md">
            <div class="row items-center no-wrap">
              <div class="icon-container" :class="`bg-${card.color}-1`">
                <q-icon :name="card.icon" :color="card.color" size="md" />
              </div>
              <div class="col q-ml-sm">
                <div class="text-h5 text-weight-bold">{{ card.value }}</div>
                <div class="text-subtitle2 text-weight-medium">{{ card.title }}</div>
              </div>
            </div>
            <div class="row items-center q-mt-sm">
              <q-chip dense :color="card.trend > 0 ? 'positive' : 'negative'" text-color="white" size="sm">
                <q-icon :name="card.trend > 0 ? 'arrow_upward' : 'arrow_downward'" size="xs" />
                {{ Math.abs(card.trend) }}%
              </q-chip>
              <span class="text-caption q-mr-xs">{{ card.subtitle }}</span>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Main Content Area -->
    <div dir="rtl" class="row q-col-gutter-md">


      <!-- Recent Transactions Table -->
      <div class="col-12">
        <q-card class="transaction-card">
          <q-card-section class="q-pb-none">
            <div class="row items-center justify-between">
              <div class="text-h6 text-weight-medium">معاملات اخیر</div>
              <q-btn color="primary" flat icon="search" />
            </div>
          </q-card-section>

          <q-card-section>
            <q-table
              :rows="recentTransactions"
              :columns="transactionColumns"
              row-key="id"
              flat
              :pagination="{ rowsPerPage: 5 }"
              :loading="loading"
              binary-state-sort
            >
              <template v-slot:body-cell-status="props">
                <q-td :props="props">
                  <q-chip :color="getStatusColor(props.value)" text-color="white" dense>
                    {{ getStatusText(props.value) }}
                  </q-chip>
                </q-td>
              </template>

              <template v-slot:body-cell-amount="props">
                <q-td :props="props">
                  <span>{{ formatPrice(props.row.amount) }}</span>
                </q-td>
              </template>

              <template v-slot:body-cell-type="props">
                <q-td :props="props">
                  <q-chip :style="{backgroundColor: getTransactionColor(props.row.type)}">
                    <span class="rounded-borders text-info">{{ getTransactionType(props.row.type) }}</span>

                  </q-chip>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { api } from "src/boot/axios";
import { ref, onMounted } from "vue";

// Loading state
const loading = ref(true);

// Dashboard statistics cards
const statsCards = ref([
  {
    title: "تعداد کاربران",
    subtitle: "نسبت به ماه گذشته",
    value: "1,256",
    icon: "people",
    color: "primary",
    trend: 12.5
  },
  {
    title: "معاملات امروز",
    subtitle: "نسبت به دیروز",
    value: "342",
    icon: "bar_chart",
    color: "secondary",
    trend: 8.3
  },
  {
    title: "درخواست‌های برداشت",
    subtitle: "در انتظار تایید",
    value: "28",
    icon: "account_balance_wallet",
    color: "warning",
    trend: -3.6
  },
  {
    title: "حجم معاملات",
    subtitle: "میلیون تومان - امروز",
    value: "54.3",
    icon: "monetization_on",
    color: "purple",
    trend: 15.2
  }
]);



// Transaction Table
const transactionColumns = [
  { name: 'id', align: 'right', label: 'شناسه', field: 'id', sortable: true },
  { name: 'user', align: 'right', label: 'کاربر', field: 'user', sortable: true },
  { name: 'type', align: 'right', label: 'نوع', field: 'type' },
  { name: 'amount', align: 'right', label: 'مبلغ (تومان)', field: 'amount', sortable: true },
  { name: 'date', align: 'right', label: 'تاریخ', field: 'date' },
  { name: 'status', align: 'right', label: 'وضعیت', field: 'status' },
];

const recentTransactions = ref([
  { id: '87123', user: 'رضا احمدی', type: 'خرید', amount: '2,500,000', date: '۱۴۰۳/۱۲/۱۵', status: 'تکمیل شده' },
  { id: '87122', user: 'فاطمه حسینی', type: 'فروش', amount: '1,200,000', date: '۱۴۰۳/۱۲/۱۵', status: 'تکمیل شده' },
  { id: '87121', user: 'مهدی رضایی', type: 'برداشت', amount: '3,000,000', date: '۱۴۰۳/۱۲/۱۴', status: 'در انتظار' },
  { id: '87120', user: 'سارا محمدی', type: 'خرید', amount: '800,000', date: '۱۴۰۳/۱۲/۱۴', status: 'تکمیل شده' },
  { id: '87119', user: 'علی کریمی', type: 'فروش', amount: '1,700,000', date: '۱۴۰۳/۱۲/۱۳', status: 'لغو شده' }
]);

const getStatusColor = (status) => {
  switch (status) {
    case 2 : return 'positive';
    case 4: return 'warning';
    default: return 'negative';
  }
};

const getStatusText = (status) => {
  return status === 4
  ? 'در انتظار'
  : status === 2
  ? 'تکمیل شده'
  : 'لفو شده'
}

const fetchTransactionsData = async() => {
  const { data } = await api.get('/get-all-transactions')
  const newTransaction = data.transactions.map(item => ({
    id: item.id,
    user: item.buyer_name,
    type: item.transaction_type,
    amount: item.rial_amount,
    date: item.shamsi_create_datetime,
    status: item.status
  }))
  recentTransactions.value = [...newTransaction]
  if(data.success){
    loading.value = false
  }
}

const getTransactionType = (type) => {
  switch(type){
    case 8 : return 'فروش';
    case 1 : return 'افزایش اعتبار';
    case 2 : return ' افزایش اعتبار';
    case 5 : return 'خرید';
    case 6 : return 'خرید';
    case 4 : return 'برداشت';
    default : return 'نامشخص'
  }
}
const getTransactionColor = (type) => {
  switch(type){
    case 8 : return 'var(--q-negative)';
    case 1 : return 'var(--q-primary)';
    case 2 : return 'var(--q-primary)';
    case 5 : return 'var(--q-positive)';
    case 6 : return 'var(--q-positive)';
    case 4 : return 'var(--q-warning)';
    default: return 'var(--q-accent)'
  }
}


// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};
onMounted(fetchTransactionsData)
</script>

<style scoped>
.dashboard-page {
  background: #f8fafc;
  min-height: 100vh;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Card Styling */
.stats-card, .chart-card, .activity-card, .transaction-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  background-color: white;
  transition: all 0.2s ease;
  overflow: hidden;
}

.stats-card:hover, .chart-card:hover, .activity-card:hover, .transaction-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

/* Stats Cards */
.icon-container {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
}

.bg-primary-1 { background-color: rgba(25, 118, 210, 0.1); }
.bg-secondary-1 { background-color: rgba(156, 39, 176, 0.1); }
.bg-warning-1 { background-color: rgba(255, 152, 0, 0.1); }
.bg-purple-1 { background-color: rgba(121, 80, 242, 0.1); }

/* Chart Improvements */
.chart-filters {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Activity Card */
.activity-card {
  height: 100%;
}

/* Responsive Adjustments */
@media (max-width: 599px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .date-filter {
    align-self: flex-end;
  }
}
</style>
