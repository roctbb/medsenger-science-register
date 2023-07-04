<template>
    <h3 class="my-3">Список проектов</h3>
    <div class="row" v-if="state.user.clinic.projects">
        <div class="col-sm-6 col-md-4 col-lg-3 mb-3 mb-sm-0">
            <div class="card" v-for="project in state.user.clinic.projects" v-bind:key="project.id">
                <div class="card-body" @click="openProject(project)">
                    <h5 class="card-title">{{ project.name }}</h5>
                </div>
            </div>
        </div>
    </div>
</template>

<script>


export default {
    name: 'ProjectsScreen',
    components: {},
    data() {
    },
    methods: {
        openProject: function (project) {
            this.managers.project.open(project)
        }
    },
    async mounted() {
    }
}
</script>

<style scoped>

</style>
