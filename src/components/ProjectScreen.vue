<template>
    <div v-if="project">
        <div class="hstack gap-3">
            <div class="me-auto">
                <h4 class="my-3">Список пациентов в проекте "{{ project.name }}"</h4>
            </div>
            <div>
                <button @click="$router.push({name: 'create_patient', params: {project_id: project.id}})"
                        class="btn btn-sm btn-primary">Добавить
                </button>
            </div>
        </div>

        <div class="row my-2" v-if="patients">
            <div class="col">
                <input type="text" placeholder="Поиск..." v-model="search_field" class="form-control"/>
            </div>
        </div>

        <div class="row py-2" v-if="patients">
            <div class="col col-sm-6 col-md-4 col-lg-3 mb-3" v-for="patient in filteredPatients"
                 v-bind:key="patient.id">
                <div class="card">
                    <div class="card-body">
                        <div class="hstack">
                            <div class="me-auto"
                                 @click="$router.push({name: 'patient', params: {project_id: project.id, id: patient.id}})">
                                <h5 class="card-title my-1">{{ patient.name }}</h5>
                            </div>
                            <div
                                @click="$router.push({name: 'edit_patient', params: {project_id: this.project.id, id: patient.id}})">
                                <font-awesome-icon :icon="['fas', 'pen']"/>
                            </div>
                        </div>

                        <p class="text-muted my-0">{{ patient.readable_birthday }}<br>{{ patient.created_by }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>


import {empty, formatDate} from "../utils/helpers";

export default {
    name: 'ProjectPatientsScreen',
    props: ['id'],
    components: {},
    data() {
        return {
            search_field: '',
            patients: undefined,
            project: undefined
        }
    },
    computed: {
        filteredPatients: function () {
            return this.patients.filter((patient) => empty(this.search_field) || patient.name.toLowerCase().includes(this.search_field.toLowerCase()))
        }
    },
    methods: {
        formatDate,
        sortPatients: function () {
            this.patients.sort((a, b) => a.name.localeCompare(b.name))
        }
    },
    async mounted() {
        this.project = this.state.user.projects.find(project => {
            console.log(project);
            return project.id === parseInt(this.id)
        })
        this.patients = await this.project.patients
    }
}
</script>

<style scoped>

</style>
