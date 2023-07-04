<template>
    <div v-if="project && patient">
        <div class="hstack gap-3">
            <div class="me-auto">
                <h4 class="my-3">{{ patient.name }}</h4>
            </div>
            <div>
                <div class="dropdown">
                    <button class="btn btn-primary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                        Добавить анкету
                    </button>
                    <ul class="dropdown-menu">
                        <li v-for="form in project.forms" v-bind:key="form.id"><a class="dropdown-item" href="#">{{ form.name }}</a></li>
                    </ul>
                </div>
            </div>
        </div>

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
