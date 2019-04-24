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
            :headers="headers"
            :items="items"
            hide-actions
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
            <template
              slot="items"
              slot-scope="{ item }"
            >
              <td>{{ item.name }}</td>
              <td>{{ item.description }}</td>
              <td>{{ item.parents }}</td>
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
export default {
  data: () => ({
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
        value: 'operation'
      },
      {
        sortable: false,
        text: '',
        value: 'operation',
        width: '200px',
        aligh: 'right'
      }
    ],
    items: [
      {
        name: 'Base Admin',
        description: 'Base Admin Role',
        parents: []
      },
      {
        name: 'Super Admin',
        description: 'Base Admin Role',
        parents: []
      }
    ]
  })
}
</script>
