<template>
    <div v-if="project">
        <div class="clearfix">
            <div class="float-start">
                <h3 class="my-3">Список пациентов в проекте "{{ project.name }}"</h3>
            </div>
            <div class="float-end align-middle">
                <button @click="addPatient" class="btn btn-sm btn-info">Добавить</button>
            </div>
        </div>


        <div class="row" v-if="patients">
            <div class="col col-sm-6 col-md-4 col-lg-3 mb-3" v-for="patient in patients" v-bind:key="patient.id">
                <div class="card">
                    <div class="card-body" @click="openPatient(patient)">
                        <h5 class="card-title">{{ patient.name }}</h5>
                        <p class="text-muted">{{ formatDate(patient.birthday) }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>


import {formatDate} from "../utils/helpers";

export default {
    name: 'ProjectPatientsScreen',
    components: {},
    data() {
        return {
            project: undefined,
            patients: []
        }
    },
    methods: {
        formatDate,
        openPatient: function (patient) {
            this.managers.project.openPatientPage(this.project, patient)
        },
        loadPatients: async function (project) {
            this.project = project
            this.patients = await this.managers.project.getPatients(project)
        },
        addPatient: function () {
            this.managers.project.addPatientPage()
        }
    },
    mounted() {
        this.event_bus.on('project-selected', this.loadPatients);
        this.event_bus.on('new-patient', (patient) => {
            this.patients.push(patient)
        });
    }
}
</script>

<style scoped>

</style>
