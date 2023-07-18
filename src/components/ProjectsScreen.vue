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
</template>

<script>


export default {
    name: 'ProjectsScreen',
    components: {},
    data() {
        return {}
    },
    async mounted() {
    }
}
</script>

<style scoped>

</style>
