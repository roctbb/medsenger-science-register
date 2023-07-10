<template>
    <div v-if="project && patient">
        <div class="hstack gap-3">
            <div class="me-auto">
                <h4 class="my-3">{{ patient.name }}</h4>
            </div>
            <div>
                <a target="_blank" class="btn btn-sm btn-success" v-if="patient.contract_id"
                   :href="medsenger_host + '/client#/?c=' + patient.contract_id">Medsenger</a>
                <a class="btn btn-sm btn-success mx-1" @click="editPatient(patient)">Изменить</a>
                <div class="dropdown d-inline">
                    <button class="btn btn-primary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                        Добавить анкету
                    </button>
                    <ul class="dropdown-menu">
                        <li v-for="form in project.forms" v-bind:key="form.id"><a class="dropdown-item"
                                                                                  href="#" @click="fillForm(form)">{{
                                form.name
                            }}</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <p class="text-muted">{{ formatDate(patient.birthday) }}</p>

        <div class="row py-2" v-if="submissions">
            <div class="col col-sm-6 col-md-4 col-lg-3 mb-3" v-for="submission in submissions"
                 v-bind:key="submission.id">
                <div class="card" @click="openSubmission(submission)">
                    <div class="card-body">
                        <h5 class="card-title">{{ findForm(submission.form_id).name }}</h5>
                        <p class="text-muted my-0">{{ formatDateTime(submission.created_on) }}</p>
                    </div>
                </div>
            </div>
        </div>

        <button @click="back()" class="btn btn-warning">Назад</button>
    </div>
</template>

<script>

import {formatDate, formatDateTime} from "../utils/helpers";

export default {
    name: 'PatientScreen',
    components: {},
    data() {
        return {
            project: undefined,
            patient: undefined,
            submissions: [],
            medsenger_host: process.env.VUE_APP_MEDSENGER_HOST
        }
    },
    methods: {
        formatDateTime,
        formatDate,
        back: function () {
            this.managers.project.open(this.project)
        },
        fillForm(form) {
            this.managers.submission.openFillPage(form)
        },
        findForm(form_id) {
            return this.project.forms.filter((form) => form_id === form.id)[0]
        },
        openSubmission(submission) {
            this.managers.submission.openSubmissionPage(this.findForm(submission.form_id), submission)
        },
        editPatient: function (patient) {
            this.managers.project.editPatientPage(patient)
        }
    },
    mounted() {
        this.event_bus.on('project-selected', (project) => {
            this.project = project
        });

        this.event_bus.on('change-screen', async (screen) => {
            if (screen === 'patient') {
                this.submissions = await this.managers.submission.getAll(this.project, this.patient)
            }
        });

        this.event_bus.on('patient-selected', async (patient) => {
            this.patient = patient
        });

        this.event_bus.on('submission-added', async (submission) => {
            this.submissions.push(submission)
        });

    }
}
</script>

<style scoped>

</style>
