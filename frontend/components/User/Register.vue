<template>
    <v-container>
        <v-layout row>
            <v-flex xs12 sm6 offset-sm3>
                <v-card>
                    <v-card-text>
                        <v-container>
                            <form @submit.prevent="register">

                                <!--Name Surname INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="name"
                                                label="Name Surname"
                                                id="name"
                                                v-model="name"
                                                type="name"
                                                required
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                                <!--EMAIL INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="email"
                                                label="Mail"
                                                id="email"
                                                v-model="email"
                                                type="email"
                                                required
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                                <!--PASSWORD INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="password"
                                                label="Password"
                                                id="password"
                                                v-model="password"
                                                type="password"
                                                required
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                                <!--CONFIRM PASSWORD INPUT FIELD-->
                                <v-layout row>
                                    <v-flex xs12>
                                        <v-text-field
                                                name="passwordConfirm"
                                                label="Confirm Password"
                                                id="passwordConfirm"
                                                v-model="passwordConfirm"
                                                type="password"
                                                required
                                                :rules="[comparePasswords]"
                                        >

                                        </v-text-field>
                                    </v-flex>
                                </v-layout>

                                <v-layout row>
                                    <v-flex xs12>
                                        <v-btn type="submit" :disabled="loading" :loading="loading">
                                            Register
                                            <span slot="loader" class="custom-loader">
                                                <v-icon light>cached</v-icon>
                                            </span>
                                        </v-btn>
                                    </v-flex>
                                </v-layout>
                            </form>
                        </v-container>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
  export default {
    components: {},
    data() {
      return {
        name: '',
        email: '',
        password: '',
        passwordConfirm: ''
      }
    },
    methods: {
      register(){
        const user = {
          name: this.name,
          email: this.email,
          password: this.password,
          passwordConfirm: this.passwordConfirm
        }
        this.$store.dispatch('register', user)
      },
    },
    computed: {
      comparePasswords() {
        return this.password !== this.passwordConfirm ? 'Passwords do not match' : true;
      },
      user(){
        return this.$store.getters.user;
      },
      loading () {
        return this.$store.getters.loading
      }
    },
    watch: {
      user(value){
        if(value !== null && value !== undefined){
          this.$router.push('/');
        }
      }
    }
  }
</script>

<style>

</style>
