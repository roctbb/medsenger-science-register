<template>
    <div v-if="project && patient">
        <div class="hstack gap-3">
            <div class="me-auto">
                <h4 class="my-3">{{ patient.name }}</h4>
            </div>
            <div>
                <a target="_blank" class="btn btn-sm btn-success" v-if="patient.contract_id"
                   :href="medsenger_host + '/client#/?c=' + patient.contract_id">Medsenger</a>
                <a class="btn btn-sm btn-success mx-1"
                   @click="$router.push({name: 'edit_patient', params: {project_id: this.project.id, id: this.patient.id}})">Изменить</a>
                <div class="dropdown d-inline">
                    <button class="btn btn-primary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                        Добавить анкету
                    </button>
                    <ul class="dropdown-menu">
                        <li v-for="form in available_forms" v-bind:key="form.id"><a class="dropdown-item text-wrap"
                                                                                    @click="$router.push({name: 'form', params: {project_id: project.id, patient_id: patient.id, form_id: form.id}})">{{
                                form.name
                            }}</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <p class="text-muted">{{ patient.readable_birthday }}</p>

        <div class="row py-2" v-if="submissions">
            <div class="col col-sm-6 col-md-4 col-lg-3 mb-3" v-for="submission in submissions"
                 v-bind:key="submission.id">
                <div class="card"
                     @click="$router.push({name: 'submission', params: {project_id: project.id, patient_id: patient.id, submission_id: submission.id}})">
                    <div class="card-body">
                        <h5 class="card-title">{{ findForm(submission.form_id).name }}</h5>
                        <small class="text-muted my-0">{{ submission.readable_created_on }}</small><br>
                        <small class="text-muted my-0">{{ submission.author }}</small>
                    </div>
                </div>
            </div>
        </div>

        <button @click="$router.back()" class="btn btn-warning">Назад</button>
    </div>
</template>

<script>

import {formatDate, formatDateTime} from "../utils/helpers";

export default {
    name: 'PatientScreen',
    props: ['project_id', 'id'],
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
        findForm(id) {
            return this.project.forms.find(form => form.id === id)
        }
    },
    computed: {
        available_forms: function () {
            return this.project.forms.filter(form => !form.specialty || this.state.user.is(form.specialty))
        }
    },
    async mounted() {
        this.project = this.state.user.projects.find(project => {
            console.log(project);
            return project.id === parseInt(this.project_id)
        })

        this.patient = (await this.project.patients).find(patient => patient.id === parseInt(this.id))
        this.submissions = await this.patient.submissions
    }
}
</script>

<style scoped>

</style>
