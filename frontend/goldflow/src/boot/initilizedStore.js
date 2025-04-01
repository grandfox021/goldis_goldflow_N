import { boot } from "quasar/wrappers";
import { useWalletStore } from "src/stores/wallet";

export default boot(() => {
  const walletStore = useWalletStore()
  walletStore.checkPrice()
})
