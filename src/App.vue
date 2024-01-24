<template>
    <div>
        <div v-if="state.loaded && auth">
            <div v-if="auth.has_auth()">
                <nav class="navbar bg-body-tertiary no-print">
                    <div class="container">

                        <a class="navbar-brand" href="#"><img class="mx-2" height="30" src="/images/icon_banner_repro_health.png" /> Регистр онкофертильности</a>

                        <div class="d-flex" v-if="state.user">
                            <button @click="logOut()" class="btn btn-secondary btn-sm">Выход</button>
                        </div>
                    </div>
                </nav>

                <div class="container">
                    <router-view></router-view>
                </div>
                <footer52></footer52>
            </div>
            <div v-else class="mainbg">
                <div class="container-fluid" style="background-color: rgba(255,255,255,0.4)">
                    <router-view></router-view>
                </div>
            </div>
        </div>
    </div>

</template>

<script>


import Footer52 from "@/components/parts/common/Footer52.vue";

export default {
    name: 'App',
    components: {Footer52},
    data() {
        return {
            auth: undefined
        }
    },
    methods: {
        logOut: function () {
            this.$router.push('/login')
            this.managers.auth.logout()

        }
    },
    async mounted() {
        this.auth = this.managers.auth
    }
}
</script>

<style>

@import url("https://fonts.googleapis.com/css?family=Roboto:100,200,300,400,500,600,700");
@import "assets/styles/buttons.css";
@import "assets/styles/printing.css";


#app {
    font-family: Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #444;
}

.accent-color {
    color: #006c88;
}

.mainbg {
    width: 100vw;
    height: 100vh;
    background-image: url("../public/images/main.jpg");
    background-size: cover;
    background-position: bottom right;
}

.navbar-brand, .navbar-brand:hover, .navbar-brand:visited {
    color: #029DAF;
}

.updated {
    border-left: 5px solid #006c88;
}

</style>
