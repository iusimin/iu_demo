<template>
  <div class="row">
    <div class="offset-md-4 col-md-4">
      <form>
        <div class="form-group">
          <label for="userName">User Name</label>
          <input type="text" class="form-control" id="userName" v-model="userName" placeholder="User Name">
        </div>
        <div class="form-group">
          <label for="exampleInputEmail1">Email address</label>
          <input
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            placeholder="Enter email"
            v-model="userEmail"
          >
          <small
            id="emailHelp"
            class="form-text text-muted"
          >We'll never share your email with anyone else.</small>
        </div>
        <div class="form-group">
          <label for="exampleInputPassword1">Password</label>
          <input
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            placeholder="Password"
            v-model="userPassword"
          >
        </div>
        <div class="form-group">
          <label for="phoneNumber">Phone Number</label>
          <input type="text" class="form-control" id="phoneNumber" v-model="userPhoneNumber" placeholder="Phone Number">
        </div>
        <button type="button" class="btn btn-primary" @click="registerUser">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data: () => ({
    userName: null,
    userEmail: null,
    userPassword: null,
    userPhoneNumber: null
  }),
  components: {},
  methods: {
    registerUser: function() {
      var vm = this;
      axios
        .post(
          "/api/users",
          {
            username: vm.userName,
            password: vm.userPassword,
            email: vm.userEmail,
            phone_number: vm.userPhoneNumber
          }
        )
        .then(alert("Register Success!"))
        .catch(error => alert(error));
    }
  }
};
</script>
