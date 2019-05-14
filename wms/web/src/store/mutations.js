// https://vuex.vuejs.org/en/mutations.html

import { MutationNames } from "@/store/constants.js";
export default {
  [MutationNames.SET_OPERATOR_WAREHOUSE](state, operator_warehouse) {
    state.operator_warehouse = operator_warehouse;
  },
  [MutationNames.SET_SEED_MODE](state, seed_mode) {
    state.seed_mode = seed_mode
  }
}
