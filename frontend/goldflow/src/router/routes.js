
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path:'',component:() => import('pages/landigPage.vue'), meta : { public: true}}
    ]
  },
  {
    path: '/authCallBack',
    component: () => import('pages/authCallBackPage.vue'),
  },
   {
     path: '/dashboard',
     component: () => import('layouts/dashboardLayout.vue'),
     children: [
       { path: '', component: () => import('pages/dashboardPage.vue') },
       {path:'wallet', component: () => import('src/pages/wallet/walletPage.vue')},
       {path:'card',component:() => import('src/pages/wallet/cardManagementPage.vue')},
       {path: 'irt', component: () => import('src/pages/wallet/irtWalletPage.vue')},
       {path: 'deposite', component: () => import('src/pages/wallet/DepositePage.vue')},
       {path: 'withdraw', component: () => import('src/pages/wallet/WithdrawPage.vue')},
       {path: 'reciept', component: () => import('src/pages/wallet/recieptPage.vue')},
       {path:'message',component:() => import('src/pages/wallet/messageDepositePage.vue')},
       {path:'Walletmessage',component:() => import('src/pages/wallet/messageForWallet.vue')},
      //  {path: 'tickets', component:() => import('src/pages/wallet/ticketsPage.vue')},
      //  {path:'ticket/:id', name:'ticketAnswer', component: () => import('src/pages/wallet/answersTicketsPage.vue')}
     ]
   },

   {
    path: '/adminDashboard',
    component: () => import('layouts/adminLayout.vue'),
    children: [
      {path:'',component:() => import('pages/admin/AdminDashboardPage.vue')},
      {path:'orders',component:() => import('pages/admin/orderManagement.vue')},
      // {path:'tickets',component:() => import('pages/admin/ticketManagement.vue')},
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('src/pages/Errors/ErrorNotFound.vue')
  }
]

export default routes
