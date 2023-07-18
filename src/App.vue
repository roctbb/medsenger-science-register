<template>
    <div>
        <nav class="navbar bg-body-tertiary">
            <div class="container">
                <a class="navbar-brand" href="#">Регистр пациентов</a>

                <div class="d-flex" v-if="state.user">
                    <button @click="logOut()" class="btn btn-secondary btn-sm">Выход</button>
                </div>
            </div>
        </nav>

        <div class="container">
            <router-view></router-view>
        </div>
    </div>

</template>

<script>


export default {
    name: 'App',
    components: {},
    data() {
        return {}
    },
    methods: {
        logOut: function () {
            this.managers.auth.logout()
            this.$router.push('/login')
        }
    },
    async mounted() {

    }
}
</script>

<style>

@import url("https://fonts.googleapis.com/css?family=Roboto:100,200,300,400,500,600,700");
@import "assets/styles/buttons.css";


#app {
    font-family: Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #444;
}

.accent-color {
    color: #006c88;
}

</style>
