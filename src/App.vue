<template>
    <div v-if="isLoaded">
        <div v-show="screen==='login'">
            <login-screen/>
        </div>
        <div v-show="screen==='projects'">
            <projects-screen/>
        </div>
        <div v-show="screen==='project-patients'">
            <project-patients-screen/>
        </div>
        <div v-show="screen==='add-patient'">
            <add-patient-screen/>
        </div>
        <div v-show="screen==='patient'">
            <patient-screen />
        </div>
    </div>
</template>

<script>


import LoginScreen from "@/components/LoginScreen.vue";
import ProjectsScreen from "@/components/ProjectsScreen.vue";
import ProjectPatientsScreen from "@/components/ProjectPatientsScreen.vue";
import AddPatientScreen from "@/components/AddPatientScreen.vue";
import PatientScreen from "@/components/PatientScreen.vue";

export default {
    name: 'App',
    components: {
        PatientScreen,
        LoginScreen,
        ProjectsScreen,
        ProjectPatientsScreen,
        AddPatientScreen
    },
    data() {
        return {
            screen: "login",
            isLoaded: false
        }
    },
    methods: {
        subscribeForEvents: function () {
            let reactors = [
                ["change-screen", this.screenChanged],
                ["state-load-done", this.stateLoaded]
            ]

            reactors.forEach((event) => {
                this.event_bus.on(event[0], event[1]);
            })
        },
        screenChanged: function (screen) {
            console.log("new state:", screen)
            this.screen = screen
        },
        stateLoaded: function () {
            this.isLoaded = true
        }
    },
    async mounted() {
        this.subscribeForEvents()

        console.log(this.$route)
    }
}
</script>

<style>

@import url("https://fonts.googleapis.com/css?family=Roboto:100,200,300,400,500,600,700");
@import "assets/styles/buttons.css";

#app {
    min-height: 100vh;
}

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
