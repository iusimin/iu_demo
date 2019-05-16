<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
  >
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        md12
      >
        <material-card
          color="green"
          title="Roles"
          text="Manage roles"
        >
          <v-data-table
            :headers="roles_table.headers"
            :items="roles_table.items"
            :loading="true"
            :pagination.sync="roles_table.pagination"
            :total-items="roles_table.total_count"
            :rows-per-page-items="[20, 30, 50, 100]"
          >
            <template
              slot="headerCell"
              slot-scope="{ header }"
            >
              <span
                class="subheading font-weight-light text-success text--darken-3"
                v-text="header.text"
              />
            </template>
            <v-progress-linear v-slot:progress color="blue" indeterminate></v-progress-linear>
            <template
              slot="items"
              slot-scope="{ item }"
            >
              <td>{{ item.name }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.parents }}</td>
              <td>{{ item.created_ts }}</td>
              <td>
                <span>
                  <v-btn
                    color="primary"
                    flat
                    small
                  >
                    Manage
                  </v-btn>
                </span>
                <span>
                  <v-btn
                    color="error"
                    flat
                    small
                  >
                    Delete
                  </v-btn>
                </span>
              </td>
            </template>
          </v-data-table>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import transform from '@/utils/transform'
export default {
  data: () => ({
    roles_table: {
      query: {},
      loading: true,
      pagination: {
        sortBy: 'created_ts',
        descending: true
      },
      total_count: 0,
      headers: [
        {
          sortable: true,
          text: 'Role Name',
          value: 'name'
        },
        {
          sortable: false,
          text: 'Description',
          value: 'description'
        },
        {
          sortable: false,
          text: 'Parents',
          value: 'parents'
        },
        {
          sortable: true,
          text: 'Created Time',
          value: 'created_ts'
        },
        {
          sortable: false,
          text: '',
          value: 'operation',
          width: '200px',
          aligh: 'right',
          static: true
        }
      ],
      items: []
    }
  }),
  watch: {
    "roles_table.pagination" (p) {
      this.getRoles()
    }
  },
  methods: {
    getRoles: function( ) {
      var vm = this
      axios.post(
        '/api/roles:list',
        transform.generateDatatableQuery(this.roles_table)
      ).then(resp => {
        console.log(resp)
        vm.roles_table.items = resp.data
      }).catch(error => {
        vm.$router.push({
          path: '/error/500'
        })
      })
    }
  }
}
</script>
