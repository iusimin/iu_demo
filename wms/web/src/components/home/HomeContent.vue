<template>
  <v-container fill-height fluid grid-list-xl>
    <v-layout wrap>
      <v-flex sm6 xs12 md6 lg4>
        <material-operation-card
          color="green"
          icon="mdi-store"
          title="入库安检"
          value="安检，区分普通货物、特殊货物、超规特货等"
          sub-icon="mdi-calendar"
          sub-text="Last 24 Hours"
          click-link="/inbound-scan"
        />
      </v-flex>
      <v-flex sm6 xs12 md6 lg4>
        <material-operation-card
          color="orange"
          icon="mdi-content-copy"
          title="分拣"
          value="1-3轮分拣库内包裹"
          sub-icon="mdi-alert"
          sub-text="Get More Space..."
          click-link="/sorter"
        />
      </v-flex>
      <v-flex sm6 xs12 md6 lg4>
        <material-operation-card
          color="red"
          icon="mdi-information-outline"
          title="播种并打单"
          value="分拣完成后以筐为单位执行"
          sub-icon="mdi-tag"
          sub-text="Tracked from Github"
          click-link="/seed"
        />
      </v-flex>

      <v-flex sm6 xs12 md6 lg4>
        <material-operation-card
          color="accent"
          icon="mdi-atom"
          title="直发打单"
          value="分拣结果为‘直接发送’的包裹执行直发打单"
          sub-icon="mdi-calendar"
          sub-text="Last 24 Hours"
          click-link="/directship"
        />
      </v-flex>
      <v-flex sm6 xs12 md6 lg4>
        <material-operation-card
          color="info"
          icon="mdi-autorenew"
          title="出库扫描"
          value="打印并贴好后程面单"
          sub-icon="mdi-alert"
          sub-text="Get More Space..."
          click-link="/outboundscan"
        />
      </v-flex>
      <v-flex sm6 xs12 md6 lg4>
        <material-operation-card
          color="warning"
          icon="mdi-azure"
          title="查询与报表"
          value="综合查询功能"
          sub-icon="mdi-tag"
          sub-text="Tracked from Github"
        />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
  }),
  props: [],
  components: {},
  computed: {},
  methods: {
  }
};
</script>

<style lang="scss">
</style>
