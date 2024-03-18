<template>
    <div v-if="project">
        <div class="hstack gap-3">
            <div class="me-auto">
                <h4 class="my-3">Список пациентов в проекте "{{ project.name }}"</h4>
                <p v-if="patients" class="my-2 text-muted">Пациентов в проекте: {{ patients.length }}</p>
            </div>
            <div>
                <button @click="$router.push({name: 'create_patient', params: {project_id: project.id}})"
                        class="btn btn-sm btn-primary">Добавить
                </button>
            </div>
        </div>

        <div class="row my-2">
            <div class="col">
                <input type="text" placeholder="Поиск..." v-model="search_field" class="form-control"/>

                <div class="form-check form-switch my-2">
                    <input class="form-check-input" type="checkbox" role="switch" v-model="table_enabled">
                    <label class="form-check-label">Таблица</label>
                </div>
            </div>
        </div>

        <div v-if="groups">
            <PatientsCards :project="project" :search_field="search_field" :groups="groups" v-if="!table_enabled"></PatientsCards>
            <PatientsTable :project="project" :search_field="search_field" :groups="groups" v-if="table_enabled"></PatientsTable>
        </div>
        <loading v-else></loading>
    </div>
</template>

<script>


import {formatDate} from "@/utils/helpers";
import Loading from "@/components/Loading.vue";
import PatientsCards from "@/components/parts/PatientsCards.vue";
import PatientsTable from "@/components/parts/PatientsTable.vue";

export default {
    name: 'ProjectPatientsScreen',
    props: ['id'],
    components: {PatientsCards, Loading, PatientsTable},
    data() {
        return {
            search_field: '',
            table_enabled: false,
            patients: undefined,
            project: undefined,
            groups: undefined
        }
    },
    methods: {
        formatDate
    },
    async mounted() {
        this.project = this.state.user.projects.find(project => {
            console.log(project);
            return project.id === parseInt(this.id)
        })
        this.patients = await this.project.patients
        this.groups = await this.project.groups

    }
}
</script>

<style scoped>

</style>
