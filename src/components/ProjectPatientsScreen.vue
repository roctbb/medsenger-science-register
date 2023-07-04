<template>
    <div v-if="project">
        <h3 class="my-3">Список пациентов в проекте "{{ project.name }}"</h3>

        <div class="row" v-if="patients">
            <div class="col-sm-6 col-md-4 col-lg-3 mb-3 mb-sm-0">
                <div class="card" v-for="patient in patients" v-bind:key="patient.id">
                    <div class="card-body" @click="openPatient(patient)">
                        <h5 class="card-title">{{ patient.name }}</h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>


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
        openPatient: function (patient) {
            this.managers.project.openPatient(patient)
        },
        loadPatients: async function (project) {
            console.log(123)
            this.project = project
            this.patients = await this.managers.project.getPatients(project)
        }
    },
    mounted() {
        this.event_bus.on('project-selected', this.loadPatients);
    }
}
</script>

<style scoped>

</style>
