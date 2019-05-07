// https://vuex.vuejs.org/en/actions.html

import api from '@/utils/api'
import {
  ActionNames,
  MutationNames
} from '@/store/constants.js';
export default {
  [ActionNames.GET_OPERATOR_WAREHOUSE](context) {
    return api.getOperatorWarehouse().then(resp => {
      context.commit(MutationNames.SET_OPERATOR_WAREHOUSE, resp.warehouse);
    });
  }
}