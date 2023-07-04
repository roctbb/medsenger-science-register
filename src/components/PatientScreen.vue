<template>
    <div v-if="project && patient">
        <h4>{{ patient.name }}</h4>
        <p class="text-muted">{{ formatDate(patient.birthday) }}</p>

        <button @click="back()" class="btn btn-warning">Назад</button>
    </div>
</template>

<script>

import {formatDate} from "../utils/helpers";

export default {
    name: 'PatientScreen',
    components: {},
    data() {
        return {
            project: undefined,
            patient: undefined,
        }
    },
    methods: {
        formatDate,
        back: function () {
            this.managers.project.open(this.project)
        }
    },
    mounted() {
        this.event_bus.on('project-selected', (project) => {
            this.project = project
        });

        this.event_bus.on('patient-selected', (patient) => {
            this.patient = patient
        });
    }
}
</script>

<style scoped>

</style>
