<template>
  <q-page class="q-pa-md">
    <div class="bg-white content-wrapper shadow-3">
      <!-- Header Banner with Gradient -->
      <div class="text-center q-pa-md">
        <div class="flex column flex-center">
          <q-icon
            size="md"
            class="q-mr-sm"
            color="primary"
            name="mdi-receipt-text-check-outline"
          />
          <h4 class="text-h5 text-primary q-my-none">فاکتورها</h4>
        </div>
      </div>

      <q-separator color="grey-3" />

      <!-- Summary Cards with Improved Design -->
      <div class="row q-pa-md q-col-gutter-md">
        <!-- Sales Card with Gradient and Chart -->
        <div class="col-12 col-md-6">
          <q-card class="summary-card sales-card" flat bordered>
            <q-card-section class="q-pb-xs">
              <div class="row justify-end items-center">
                <div class="row items-center">
                  <span class="text-accent text-weight-medium">فروش سریع</span>
                  <q-icon
                    name="arrow_back"
                    color="primary"
                    size="xs"
                    class="q-ml-xs"
                  />
                </div>
              </div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <div class="row justify-between items-center">
                <div>
                  <div class="text-weight-bold text-h6">۱۲۸,۸۹۴ تومان</div>
                  <div class="text-grey-8">(۵.۵۲ گرم)</div>
                </div>
                <div class="row items-center">
                  <div class="mini-chart q-mr-md">
                    <svg viewBox="0 0 100 40" width="80" height="30">
                      <path
                        d="M0,30 L20,25 L40,28 L60,15 L80,20 L100,10"
                        fill="none"
                        stroke="#FFC107"
                        stroke-width="2"
                      />
                      <path
                        d="M0,30 L20,25 L40,28 L60,15 L80,20 L100,10 L100,40 L0,40 Z"
                        fill="rgba(255, 193, 7, 0.1)"
                      />
                    </svg>
                  </div>
                  <div class="text-h6 text-accent">۱ فروش</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Purchase Card with Gradient and Chart -->
        <div class="col-12 col-md-6">
          <q-card class="summary-card purchase-card" flat bordered>
            <q-card-section class="q-pb-xs">
              <div class="row justify-end items-center">
                <div class="row items-center">
                  <span class="text-accent text-weight-medium">خرید سریع</span>
                  <q-icon
                    name="arrow_back"
                    color="primary"
                    size="xs"
                    class="q-ml-xs"
                  />
                </div>
              </div>
            </q-card-section>

            <q-card-section class="q-pt-none">
              <div class="row justify-between items-center">
                <div>
                  <div class="text-weight-bold text-h6">۱۴۶,۲۹۴ تومان</div>
                  <div class="text-grey-8">(۵.۵۲ گرم)</div>
                </div>
                <div class="row items-center">
                  <div class="mini-chart q-mr-md">
                    <svg viewBox="0 0 100 40" width="80" height="30">
                      <path
                        d="M0,20 L20,15 L40,25 L60,10 L80,15 L100,5"
                        fill="none"
                        stroke="#2196F3"
                        stroke-width="2"
                      />
                      <path
                        d="M0,20 L20,15 L40,25 L60,10 L80,15 L100,5 L100,40 L0,40 Z"
                        fill="rgba(33, 150, 243, 0.1)"
                      />
                    </svg>
                  </div>
                  <div class="text-h6 text-accent">۲ خرید</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Filter and Tools Section with Better Layout -->
      <div class="q-px-md q-pb-md">
        <q-card class="filter-card" flat bordered>
          <q-card-section>
            <div class="justify-between items-center q-mb-md">
              <div class="flex items-center">
                <q-btn v-show="!showSearch" color="primary" class="text-white btn-with-icon"  @click="toggleSearch">
                  <q-icon left name="search" />
                  جستجو
                </q-btn>
                <!-- Animated Search Bar -->
                  <q-slide-transition>
                    <div v-show="showSearch" class="q-mt-md">
                      <q-input
                        v-model="searchQuery"
                        outlined
                        dense
                        placeholder='جستجو ...'
                        class="search-input"
                        @update:model-value="filterReceipts"
                        v-persian-numbers
                      >
                        <template v-slot:prepend>
                          <q-icon name="search" color="primary" />
                        </template>
                        <template v-slot:append>
                          <q-btn flat round dense icon="close" @click="clearSearch"  />
                        </template>
                      </q-input>
                    </div>
                  </q-slide-transition>
              </div>
            </div>

            <!-- Invoice Table with Enhanced Design -->
            <div class="q-mt-md">
              <!-- First Invoice Row -->
              <div
                v-for="item in filteredReceipts"
                :key="item.id"
                class="invoice-item q-mb-md"
              >
                <div class="row justify-between items-center q-mb-xs">
                  <div class="row q-gutter-sm">
                    <q-chip
                      dense
                      color="positive"
                      text-color="white"
                      class="chip-status"
                    >
                      <q-icon name="check_circle" size="xs" class="q-mr-xs" />
                      تایید شده
                    </q-chip>
                  </div>
                  <div class="row items-center">
                    <span
                      v-if="item.seller !== 'گلدیس'"
                      class="text-weight-medium text-positive"
                    >
                      خرید از ما
                      <q-icon
                        name="inventory"
                        class="q-ml-xs"
                        color="positive"
                      />
                    </span>
                    <span
                      v-if="item.seller === 'گلدیس'"
                      class="text-weight-medium text-negative"
                      >فروش به ما
                      <q-icon
                        name="inventory"
                        class="q-ml-xs"
                        color="negative"
                      />
                    </span>
                  </div>
                </div>

                <q-card bordered class="invoice-card">
                  <div class="row justify-between q-px-md q-py-md">
                    <div class="col-12 col-sm-4">
                      <div class="text-caption text-grey-7">خریدار:</div>
                      <div class="text-weight-medium q-mt-xs">
                        {{ item.seller }}
                      </div>
                    </div>
                    <div class="col-12 col-sm-4">
                      <div class="text-caption text-grey-7">فروشنده:</div>
                      <div class="text-weight-medium q-mt-xs">
                        {{ item.customer }}
                      </div>
                    </div>
                    <div class="col-12 col-sm-4">
                      <div class="text-caption text-grey-7">شناسه:</div>
                      <div class="text-weight-medium q-mt-xs">
                        {{ item.sellId }}
                      </div>
                    </div>
                  </div>

                  <q-separator />

                  <div
                    v-show="item.openDetails"
                    class="row justify-between q-px-md q-py-md"
                  >
                    <div class="col-12 col-sm-4">
                      <div class="text-caption text-grey-7">زمان:</div>
                      <div class="text-weight-medium q-mt-xs">
                        {{ item.time }}
                      </div>
                    </div>
                    <div class="col-12 col-sm-4">
                      <div class="text-caption text-grey-7">میزان:</div>
                      <div class="text-weight-medium q-mt-xs">
                        {{ item.goldAmount }}
                        <span>گرم </span>
                      </div>
                    </div>
                    <div class="col-12 col-sm-4">
                      <div class="text-caption text-grey-7">کارمزد:</div>
                      <div class="text-weight-medium q-mt-xs">{{ formatPrice(item.fee) }}
                        <span>تومان</span>
                      </div>
                    </div>
                  </div>

                  <q-separator />

                  <div class="row justify-between q-px-md q-py-md">
                    <div class="col-12 col-sm-6">
                      <div class="text-caption text-grey-7">قیمت هر گرم:</div>
                      <div class="text-weight-medium q-mt-xs">
                        {{ formatPrice(item.currentPrice) }}
                      </div>
                    </div>
                    <div class="col-12 col-sm-6">
                      <div class="text-caption text-grey-7">جمع کل:</div>
                      <div class="text-weight-bold text-primary q-mt-xs">
                        {{ formatPrice(item.totalPrice) }}
                      </div>
                    </div>
                  </div>

                  <div class="text-center q-mt-sm q-pb-sm">
                    <q-btn
                      @click="item.openDetails = !item.openDetails"
                      flat
                      color="primary"
                      class="details-btn"
                    >
                      جزئیات بیشتر
                      <q-icon
                        v-if="item.openDetails"
                        name="expand_less"
                        class="q-ml-xs"
                      />
                      <q-icon
                        v-if="!item.openDetails"
                        name="expand_more"
                        class="q-ml-xs"
                      />
                    </q-btn>
                  </div>
                </q-card>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { api } from "src/boot/axios";
import { persianToEnglish } from "src/composable/useNumberUtils";


const userId = ref('')
const customerName = ref('')
const showSearch = ref(false);
const searchQuery = ref("");
const filteredReceipts = ref([]);
const recieptList = ref([]);
const fetchReciept = async() => {
  try{
    const { data } = await api.get(`/get-transactions-by-user/${userId.value}`)
    const newReceipt = data.map(transaction => ({
      seller: transaction.seller_name || "Unknown",
      customer: transaction.buyer_name ,
      sellId: transaction.payment_ref_id || "N/A",
      time: transaction.shamsi_create_datetime || "N/A",
      goldAmount: transaction.gold_amount || 0,
      currentPrice: transaction.asset_price_at_transaction_time/10 || 0,
      totalPrice: transaction.rial_amount/10 || 0,
      openDetails: false,
      fee: transaction.goldis_fee
    }));
    console.log(newReceipt);
    recieptList.value = [...newReceipt]
    filteredReceipts.value = recieptList.value
  }catch(err){
    console.log(err)
  }
}

const toggleSearch = () => {
  showSearch.value = !showSearch.value;
  if (!showSearch.value) {
    searchQuery.value = ""; // Clear search when hiding
    filteredReceipts.value = recieptList.value; // Reset list
  }
};

const clearSearch = () => {
  searchQuery.value = "";
  filteredReceipts.value = recieptList.value; // Reset the list
  showSearch.value = false
};

// Filter receipts based on user input
const filterReceipts = () => {
  const query = persianToEnglish(searchQuery.value.toLowerCase());
  filteredReceipts.value = recieptList.value.filter(
    (item) =>
      item.seller.toLowerCase().includes(query) ||
      item.customer.toLowerCase().includes(query) ||
      item.sellId.toLowerCase().includes(query)
  );
};

// Initially, show all receipts
filteredReceipts.value = recieptList.value;



const fetchUser = async() => {
  try{
    const { data } = await api.get("/get-user-info")
    userId.value = data.user_info.id
    customerName.value = data.user_info.first_name
  }catch(err){
    console.log(err);
  }
}


onMounted(async () => {
  await fetchUser();
  await fetchReciept();
});

// Format price with Persian numerals
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(price);
};

</script>

<style lang="scss" scoped>
.content-wrapper {
  border-radius: 16px;
  overflow: hidden;
}

.header-banner {
  background: linear-gradient(to right, #f5f7fa, #e4e8f0);
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.summary-card {
  border-radius: 12px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }
}

.sales-card {
  background: linear-gradient(to right, #fffaf1, #fff5e6);
  border: 1px solid #ffe0b2;
}

.purchase-card {
  background: linear-gradient(to right, #e3f2fd, #f0f8ff);
  border: 1px solid #b3e5fc;
}

.filter-card {
  border-radius: 12px;
}

.btn-with-icon {
  border-radius: 8px;
  transition: all 0.2s ease;
  min-width: 200px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }
}

.invoice-item {
  transition: all 0.3s ease;

  &:hover .invoice-card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

.invoice-card {
  border-radius: 10px;
  transition: all 0.3s ease;
}

.chip-label {
  border-radius: 6px;
  font-weight: 500;
}

.chip-status {
  border-radius: 6px;
  font-weight: 500;
}

.details-btn {
  transition: all 0.2s ease;

  &:hover {
    background-color: rgba(25, 118, 210, 0.1);
    border-radius: 8px;
  }
}


.slow-down {
  transition: opacity 20s ease 2s;
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

@media (max-width: 599px) {
  .row > div {
    margin-bottom: 12px;
  }
}
</style>
