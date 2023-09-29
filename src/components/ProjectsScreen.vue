<template>
    <h4 class="my-3">Список проектов</h4>
    <div class="row" v-if="state.user && state.user.projects">
        <div class="col-sm-6 col-md-4 col-lg-3 mb-3 mb-sm-0">
            <div class="card" v-for="project in state.user.projects" v-bind:key="project.id">
                <div class="card-body" @click="$router.push({name: 'project', params: {id: project.id}})">
                    <h5 class="card-title">{{ project.name }}</h5>
                </div>
            </div>
        </div>
    </div>
    <loading v-else></loading>
</template>

<script>


import Loading from "@/components/Loading.vue";

export default {
    name: 'ProjectsScreen',
    components: {Loading},
    data() {
        return {
            global_state: undefined
        }
    },
    async mounted() {
        this.global_state = this.state
    },
    watch: {
        global_state() {
            if (this.state.user && this.state.user.projects) {
                if (this.state.user.projects.length === 1) {
                    this.$router.push({name: 'project', params: {id: this.state.user.projects[0].id}})
                }
            }
        }

    }


}
</script>

<style scoped>

</style>
