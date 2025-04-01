<template>
  <q-page class="q-pa-md">
    <!-- Header Section with Title, Search and Refresh Controls -->
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-8">
        <div class="text-h5 text-primary q-mb-sm">مدیریت معاملات</div>
        <div class="row q-col-gutter-sm items-center">
          <div class="col-12 col-sm-6">
            <q-select
              v-model="selectedStatus"
              :options="statusOptions"
              outlined
              dense
              emit-value
              map-options
              option-label="label"
              option-value="value"
              label="فیلتر بر اساس وضعیت"
              class="full-width"
              clearable
            >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps" @click="selectedStatus = scope.opt.value">
                <q-item-section avatar>
                  <q-badge :color="getStatusColor(scope.opt.value)" />
                </q-item-section>
                <q-item-section>{{ scope.opt.label }}</q-item-section>
              </q-item>
            </template>
            </q-select>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-4 flex justify-end items-start q-gutter-sm">
        <q-btn
          icon="refresh"
          class="q-px-md spe text-accent"
          :loading="refreshLoading"
          @click="refreshData"
        />
        <q-btn-dropdown
          color="secondary"
          icon="settings"
          flat
        >
          <q-list>
            <q-item clickable v-close-popup @click="toggleAutoRefresh">
              <q-item-section avatar>
                <q-icon :name="autoRefreshActive ? 'timer_off' : 'timer'" />
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ autoRefreshActive ? 'توقف بروزرسانی خودکار' : 'بروزرسانی خودکار' }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </div>
    </div>

    <!-- Table Card -->
    <q-card class="q-mt-md shadow-3 orders-table-card">
      <q-card-section>
        <!-- Top Pagination -->
        <div class="row justify-between q-mb-sm">
          <div class="text-subtitle1 text-weight-medium">
            <q-chip outline color="primary">
              <q-icon name="list" class="q-mr-xs" />
              {{ filteredOrders.length }} معامله
            </q-chip>
          </div>
        </div>

        <!-- Orders Table -->
        <q-table
          class="orders-table"
          :rows="filteredOrders"
          :columns="columns"
          row-key="id"
          :loading="loading"
          :pagination="pagination"
          @request="onRequest"
          binary-state-sort
          :visible-columns="visibleColumns"
          bordered
          flat
          :separator="separator"
          :row-class="rowClass"
        >
          <!-- Loading Indicator -->
          <template v-slot:loading>
            <q-inner-loading showing color="primary">
              <q-spinner size="50px" color="primary" />
              <div class="q-mt-sm text-primary">در حال بارگذاری اطلاعات...</div>
            </q-inner-loading>
          </template>

          <!-- Custom Header -->
          <template v-slot:header="props">
            <q-tr :props="props">
              <q-th v-for="col in props.cols" :key="col.name" :props="props" class="text-weight-bold">
                {{ col.label }}
                <q-icon v-if="col.sortable" name="arrow_upward" size="xs" class="q-ml-xs" :class="{ 'rotate-180': props.cols.indexOf(col) === sortedColumn && sortOrder === 'desc', 'invisible': props.cols.indexOf(col) !== sortedColumn }" />
              </q-th>
            </q-tr>
          </template>

          <!-- Empty State -->
          <template v-slot:no-data>
            <div class="full-width row flex-center q-py-lg">
              <div class="text-center">
                <q-icon name="sentiment_dissatisfied" size="50px" color="grey-7" />
                <div class="text-h6 text-grey-7 q-mt-sm">هیچ معامله‌ای یافت نشد</div>
                <div class="text-grey-7 q-mt-xs">می‌توانید فیلترها را تغییر دهید یا صفحه را بروزرسانی کنید</div>
                <q-btn color="primary" label="نمایش همه معاملات" class="q-mt-sm" @click="clearFilters" />
              </div>
            </div>
          </template>

          <!-- Status Cell -->
          <template v-slot:body-cell-status="props">
            <q-td :props="props">
              <q-badge
                :color="getStatusColor(props.value)"
                class="status-badge q-py-xs q-px-sm"
                outline
              >
                <q-tooltip>{{ getStatusDescription(props.value) }}</q-tooltip>
                {{ getStatusText(props.value) }}
              </q-badge>
            </q-td>
          </template>

          <!-- Amount Cell -->
          <template v-slot:body-cell-amount="props">
            <q-td :props="props" class="text-weight-medium">
              {{ formatCurrency(props.value) }}
              <q-tooltip>{{ formatCurrency(props.value) }}</q-tooltip>
            </q-td>
          </template>


          <!-- Actions Cell -->
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <!-- Desktop View -->
              <div  class="gt-xs row q-gutter-xs justify-center">
                <q-btn
                  v-if="props.row.status === 'pending'"
                  color="green"
                  icon="check"
                  outline
                  size="sm"
                  @click="confirmAction('تأیید', () => approveOrder(props.row.id))"
                  :loading="actionLoading.type === 'approve' && actionLoading.id === props.row.id"
                >
                  <q-tooltip>تأیید معامله</q-tooltip>
                </q-btn>

                <q-btn
                  v-if="props.row.status === 'pending'"
                  color="red"
                  icon="close"
                  outline
                  size="sm"
                  @click="confirmAction('رد', () => rejectOrder(props.row.id))"
                  :loading="actionLoading.type === 'reject' && actionLoading.id === props.row.id"
                >
                  <q-tooltip>رد معامله</q-tooltip>
                </q-btn>

                <q-btn
                  v-if="props.row.status !== 'canceled'"
                  color="orange"
                  icon="cancel"
                  outline
                  size="sm"
                  @click="confirmAction('لغو', () => cancelOrder(props.row.id))"
                  :loading="actionLoading.type === 'cancel' && actionLoading.id === props.row.id"
                >
                  <q-tooltip>لغو معامله</q-tooltip>
                </q-btn>

                <q-btn
                  color="blue"
                  icon="info"
                  outline
                  size="sm"
                  @click="showOrderDetails(props.row)"
                >
                  <q-tooltip>مشاهده جزئیات</q-tooltip>
                </q-btn>
              </div>

              <!-- Mobile View -->
              <div class="lt-sm">
                <q-btn-dropdown color="primary" label="عملیات" size="sm" flat icon="more_vert">
                  <q-list>
                    <q-item v-if="props.row.status === 'pending'" clickable v-close-popup @click="confirmAction('تأیید', () => approveOrder(props.row.id))">
                      <q-item-section avatar>
                        <q-icon color="green" name="check" />
                      </q-item-section>
                      <q-item-section>تأیید معامله</q-item-section>
                    </q-item>

                    <q-item v-if="props.row.status === 'pending'" clickable v-close-popup @click="confirmAction('رد', () => rejectOrder(props.row.id))">
                      <q-item-section avatar>
                        <q-icon color="red" name="close" />
                      </q-item-section>
                      <q-item-section>رد معامله</q-item-section>
                    </q-item>

                    <q-item v-if="props.row.status !== 'canceled'" clickable v-close-popup @click="confirmAction('لغو', () => cancelOrder(props.row.id))">
                      <q-item-section avatar>
                        <q-icon color="orange" name="cancel" />
                      </q-item-section>
                      <q-item-section>لغو معامله</q-item-section>
                    </q-item>

                    <q-separator />

                    <q-item clickable v-close-popup @click="showOrderDetails(props.row)">
                      <q-item-section avatar>
                        <q-icon color="blue" name="info" />
                      </q-item-section>
                      <q-item-section>مشاهده جزئیات</q-item-section>
                    </q-item>
                  </q-list>
                </q-btn-dropdown>
              </div>
            </q-td>
          </template>
        </q-table>

      </q-card-section>
    </q-card>

    <!-- Order Details Dialog -->
      <q-dialog v-model="orderDetailsDialog" persistent transition-show="scale" transition-hide="scale">
        <q-card class="order-details-card" style="min-width: 380px; max-width: 500px; border-radius: 12px">
          <q-card-section class="bg-primary text-white q-pb-sm">
            <div class="row items-center no-wrap">
              <div class="col">
                <div class="text-h6 text-weight-bold">جزئیات معامله</div>
                <div class="text-caption" v-if="selectedOrder">
                  <q-icon name="event" size="xs" class="q-mr-xs" />{{ selectedOrder.date }}
                </div>
              </div>
              <q-btn icon="close" flat round dense v-close-popup class="bg-white-4" />
            </div>
          </q-card-section>

          <q-card-section v-if="selectedOrder" class="q-pa-md">
            <!-- Status Badge at the top -->
            <div class="text-center q-mb-md">
              <q-badge
                :color="getStatusColor(selectedOrder.status)"
                class="status-badge q-py-sm q-px-md text-subtitle1"
                outline
              >
                <q-icon :name="getStatusIcon(selectedOrder.status)" class="q-mr-xs" />
                {{ getStatusText(selectedOrder.status) }}
              </q-badge>
            </div>

            <!-- Order Summary Card -->
            <q-card flat bordered class="summary-card q-mb-md">
              <q-card-section class="q-pa-sm bg-grey-2">
                <div class="row items-center">
                  <q-icon name="person" color="primary" size="sm" class="q-mr-xs" />
                  <div class="text-subtitle1 text-weight-medium">{{ selectedOrder.name }}</div>
                </div>
                <div class="row items-center q-mt-xs">
                  <q-icon name="payment" color="primary" size="sm" class="q-mr-xs" />
                  <div class="text-h6 text-weight-bold">{{ formatCurrency(selectedOrder.amount) }}</div>
                </div>
              </q-card-section>
            </q-card>

            <!-- Details List -->
            <q-list bordered separator class="rounded-borders">
              <q-item>
                <q-item-section avatar>
                  <q-icon name="tag" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label caption>شناسه معامله</q-item-label>
                  <q-item-label class="text-weight-medium">{{ selectedOrder.id }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-btn flat round size="sm" icon="content_copy" @click="copyToClipboard(selectedOrder.id)">
                    <q-tooltip>کپی شناسه</q-tooltip>
                  </q-btn>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section avatar>
                  <q-icon name="category" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label caption>نوع</q-item-label>
                  <q-item-label class="text-weight-medium">{{ selectedOrder.type }}</q-item-label>
                </q-item-section>
              </q-item>

            </q-list>
          </q-card-section>

          <q-card-actions align="left" class="bg-grey-2 q-pa-md">
            <div class="row full-width justify-between items-center">

              <div v-if="selectedOrder">
                <q-btn-group flat>
                  <q-btn
                    v-if="selectedOrder.status === 'pending'"
                    color="positive"
                    icon="check_circle"
                    label="تأیید"
                    @click="confirmAction('approve', selectedOrder.id)"
                    class="q-mr-sm"
                  />
                  <q-btn
                    v-if="selectedOrder.status === 'pending'"
                    color="negative"
                    icon="cancel"
                    label="رد"
                    @click="confirmAction('reject', selectedOrder.id)"
                    class="q-mr-sm"
                  />
                  <q-btn
                    v-if="selectedOrder.status !== 'canceled'"
                    color="warning"
                    icon="remove_circle"
                    label="لغو"
                    @click="confirmAction('cancel', selectedOrder.id)"
                  />
                </q-btn-group>

              </div>
              <q-btn flat color="grey" icon="arrow_back" label="بستن" v-close-popup />
            </div>
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Confirmation Dialog -->
      <q-dialog v-model="confirmDialog" persistent>
        <q-card style="min-width: 300px">
          <q-card-section class="row items-center bg-primary">
            <div class="text-h6 text-info">تأیید عملیات</div>
            <q-space />
            <q-btn icon="close" class="text-info" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="text-center">
            آیا از {{ confirmMessage }} این معامله اطمینان دارید؟
          </q-card-section>

          <q-card-actions align="center">
            <q-btn flat label="انصراف" color="primary" v-close-popup />
            <q-btn flat label="تأیید" color="negative" @click="executeConfirmedAction" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

  </q-page>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import { useQuasar } from "quasar";
import { api } from "src/boot/axios";

const $q = useQuasar();
const loading = ref(false);
const refreshLoading = ref(false);
const searchText = ref('');
const selectedStatus = ref('');
const sortedColumn = ref(0);
const sortOrder = ref('asc');
const autoRefreshActive = ref(false);
const autoRefreshInterval = ref(null);
const visibleColumns = ref(['id', 'user', 'amount', 'type', 'status', 'date', 'actions','hy']);
const actionLoading = ref({ id: null, type: null });
const separator = ref('cell');

// Dialogs
const orderDetailsDialog = ref(false);
const selectedOrder = ref(null);
const confirmDialog = ref(false);
const confirmMessage = ref('');
const confirmedAction = ref(null);



const statusOptions = [
  { label: 'تکمیل شده', value: 'completed', color: 'green', itemProps: { clickable: true } },
  { label: 'در انتظار', value: 'pending', color: 'orange', itemProps: { clickable: true } },
  { label: 'لغو شده', value: 'reject', color: 'red', itemProps: { clickable: true } }
];

const columns = [
  { name: "id", label: "شناسه", field: row => row.id, align: "left", sortable: true },
  { name: "user", label: "کاربر", field: "name", align: "left", sortable: true },
  { name: "amount", label: "مبلغ", field: "amount", align: "right", sortable: true },
  { name: "status", label: "وضعیت", field: row => row.status, align: "center", sortable: true },
  { name: "date", label: "تاریخ", field: "date", align: "right", sortable: true },
  { name: "actions", label: "عملیات", align: "center",required: true },
];

const orders = ref([
  { id: 1, name: "علی محمدی", amount: 5000000, type: "خرید", status: "pending", date: "1402/12/20" },
  { id: 2, name: "زهرا احمدی", amount: 12000000, type: "فروش", status: "completed", date: "1402/12/19" },
  { id: 3, name: "مهدی رضایی", amount: 7500000, type: "خرید", status: "canceled", date: "1402/12/18" },
]);

// Alternating row colors
const rowClass = (row, index) => {
  return index % 2 === 0 ? 'bg-grey-1' : '';
};

// Computed filtered orders based on search text and selected status
const filteredOrders = computed(() => {
  let result = [...orders.value];

  // Filter by status
  if (selectedStatus.value) {
    result = result.filter(order => order.status === selectedStatus.value);
  }

  // Filter by search text
  if (searchText.value.trim()) {
    const searchLower = searchText.value.toLowerCase();
    result = result.filter(order =>
      order.id.toString().includes(searchLower) ||
      order.name.toLowerCase().includes(searchLower) ||
      order.type.toLowerCase().includes(searchLower) ||
      order.status.toLowerCase().includes(searchLower)
    );
  }

  return result;
});


// Methods
const fetchOrders = async () => {
  loading.value = true;
  try {
    const { data } = await api.get('/get-withdrawl-requests')

      const newReciept = data.withdrawal_requests.map(item => ({
        id: item.id,
        name: item.full_name,
        amount: item.amount,
        status: item.status,
        date: item.created_at
      }))
      orders.value = [...newReciept]


  } catch (err) {
    showNotification('خطا در دریافت اطلاعات', 'negative');
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const refreshData = async () => {
  refreshLoading.value = true;
  await fetchOrders();
  refreshLoading.value = false;
  showNotification('اطلاعات با موفقیت بروزرسانی شد', 'positive');
};

const approveOrder = async (orderId) => {
  actionLoading.value = { id: orderId, type: 'approve' };
  try {
    // In a real app, this would call a real API endpoint
    await api.patch(`/update-withdrawal-request/${orderId}`,{
      status: "approve"
    });
    // Update local state to reflect changes
    const orderIndex = orders.value.findIndex(o => o.id === orderId);
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = 'completed';
    }
    showNotification('سفارش با موفقیت تأیید شد', 'positive');
  } catch (error) {
    showNotification('خطا در تأیید سفارش', 'negative');
    console.error(error);
  } finally {
    actionLoading.value = { id: null, type: null };
  }
};

const rejectOrder = async (orderId) => {
  actionLoading.value = { id: orderId, type: 'reject' };
  try {
    await api.patch(`/update-withdrawal-request/${orderId}`,{
      status: "reject"
    });
    const orderIndex = orders.value.findIndex(o => o.id === orderId);
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = 'reject';
    }
    showNotification('سفارش با موفقیت رد شد', 'negative');
  } catch (error) {
    showNotification('خطا در رد سفارش', 'negative');
    console.error(error);
  } finally {
    actionLoading.value = { id: null, type: null };
  }
};

const cancelOrder = async (orderId) => {
  actionLoading.value = { id: orderId, type: 'cancel' };
  try {
    await api.patch(`/update-withdrawal-request/${orderId}`,{
      status: "reject"
    });
    const orderIndex = orders.value.findIndex(o => o.id === orderId);
    if (orderIndex !== -1) {
      orders.value[orderIndex].status = 'reject';
    }
    showNotification('سفارش با موفقیت لغو شد', 'warning');
  } catch (error) {
    showNotification('خطا در لغو سفارش', 'negative');
    console.error(error);
  } finally {
    actionLoading.value = { id: null, type: null };
  }
};

const getStatusColor = (status) => {
  return status === "completed"
    ? "green"
    : status === "pending"
    ? "orange"
    : "red";
};

const getStatusText = (status) => {
  return status === "completed"
    ? "تکمیل شده"
    : status === "pending"
    ? "در انتظار"
    : "لغو شده";
};

const getStatusDescription = (status) => {
  return status === "completed"
    ? "این معامله با موفقیت تکمیل شده است"
    : status === "pending"
    ? "این معامله در انتظار تایید است"
    : "این معامله لغو شده است";
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat('fa-IR', {
    style: 'currency',
    currency: 'IRR',
    maximumFractionDigits: 0
  }).format(value);
};

const showNotification = (message, type = 'info') => {
  $q.notify({
    message,
    color: type,
    icon: type === 'positive' ? 'check_circle' :
          type === 'negative' ? 'error' :
          type === 'warning' ? 'warning' : 'info',
    position: 'top-right',
    timeout: 2500,
    actions: [{ icon: 'close', color: 'white' }],
    progress: true,
    textColor: 'white',
    multiLine: message.length > 30,
    classes: 'notification-popup'
  });
};


const clearFilters = () => {
  searchText.value = '';
  selectedStatus.value = null;
};

const toggleAutoRefresh = () => {
  autoRefreshActive.value = !autoRefreshActive.value;

  if (autoRefreshActive.value) {
    autoRefreshInterval.value = setInterval(refreshData, 30000); // Every 30 seconds
    showNotification('بروزرسانی خودکار هر 30 ثانیه فعال شد', 'info');
  } else {
    clearInterval(autoRefreshInterval.value);
    showNotification('بروزرسانی خودکار غیرفعال شد', 'info');
  }
};

const showOrderDetails = (order) => {
  selectedOrder.value = order;
  orderDetailsDialog.value = true;
};

const confirmAction = (message, action) => {
  confirmMessage.value = message;
  confirmedAction.value = action;
  confirmDialog.value = true;
};

const executeConfirmedAction = () => {
  if (confirmedAction.value) {
    confirmedAction.value();
    confirmedAction.value = null;
  }
};



// Lifecycle hooks
onMounted(() => {
  fetchOrders();
});

onUnmounted(() => {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value);
  }
});


// Methods
const getStatusIcon = (status) => {
  const icons = {
    pending: 'pending',
    approved: 'check_circle',
    rejected: 'cancel',
    canceled: 'remove_circle',
    completed: 'task_alt'
  };
  return icons[status] || 'help';
};

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);
  $q.notify({
    message: 'کپی شد',
    color: 'primary',
    icon: 'content_copy',
    position: 'top',
    timeout: 1000
  });
};



</script>

<style scoped>
.orders-table-card {
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.orders-table .q-table__top,
.orders-table .q-table__bottom {
  padding: 12px 16px;
}

.orders-table thead tr th {
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.03);
  transition: background-color 0.2s ease;
}

.orders-table tbody tr {
  transition: background-color 0.2s ease;
}
.order-details-card {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}
.status-badge {
  border-radius: 16px;
  font-weight: 500;
}
.summary-card {
  border-radius: 8px;
  transition: all 0.3s;
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  }
}

.spe{
  background-color: transparent;
}
</style>
