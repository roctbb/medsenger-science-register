<template>
    <div v-if="project && patient && form">

        <h4 class="my-3">{{ patient.name }}: {{ form.name }} <small
            v-if="this.disabled"> ({{ formatDateTime(this.submission.created_on) }})</small></h4>

        <p>{{ form.description }}</p>

        <div class="alert alert-warning" v-if="error">
            {{ error }}
        </div>

        <div class="card mb-3" v-for="part in form.parts" v-bind:key="part.id">
            <div class="card-body">
                <h5 class="card-title">{{ part.name }}</h5>

                <div v-for="field in part.fields" v-bind:key="field.id">
                    <div class="row mb-3" v-if="!field.show_if || submission.answers[field.show_if]">
                        <label class="col-sm-4 col-form-label" :class="{ required: field.required }">{{
                                field.text
                            }}</label>
                        <div class="col-sm-8">
                            <input v-if="field.type === 'string'" type="text" class="form-control"
                                   v-model="submission.answers[field.id]"
                                   v-bind:required="field.required" v-bind:disabled="disabled">

                            <input v-if="field.type === 'integer'" type="number" step="1" class="form-control"
                                   v-model="submission.answers[field.id]"
                                   v-bind:required="field.required" v-bind:disabled="disabled">

                            <input v-if="field.type === 'float'" type="number" step="0.01" class="form-control"
                                   v-model="submission.answers[field.id]"
                                   v-bind:required="field.required" v-bind:disabled="disabled">

                            <textarea v-if="field.type === 'text'" class="form-control" v-model="submission.answers[field.id]"
                                      v-bind:required="field.required" v-bind:disabled="disabled"></textarea>


                            <VueDatePicker v-if="field.type === 'date'" auto-apply model-type="yyyy-MM-dd"
                                           v-model="submission.answers[field.id]"
                                           input-class-name="form-control" text-input
                                           :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                                           select-text="Выбрать" cancel-text="Закрыть" v-bind:required="field.required"
                                           v-bind:disabled="disabled"/>

                            <div v-if="field.type === 'radio'">
                                <div v-for="(value, option) in field.params.options"
                                     v-bind:key='option'
                                     class="form-check">
                                    <input class="form-check-input" type="radio"
                                           :value="value" v-model="submission.answers[field.id]" v-bind:disabled="disabled">
                                    <label class="form-check-label">
                                        {{ option }}
                                    </label>
                                </div>
                            </div>

                            <div class="form-check" v-if="field.type === 'checkbox'">
                                <input class="form-check-input" type="checkbox" v-model="submission.answers[field.id]"
                                       v-bind:disabled="disabled">
                            </div>

                            <div class="form-text" v-if="field.description">{{ field.description }}</div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

    </div>

    <div class="my-3">
        <button @click="save()" class="btn btn-primary" v-if="!disabled">Сохранить</button>
        <button @click="back()" class="btn btn-warning mx-1">Назад</button>
    </div>

</template>

<script>

import VueDatePicker from "@vuepic/vue-datepicker";
import {formatDateTime} from "../utils/helpers";
import Submission from "@/models/Submission";

export default {
    name: 'FormScreen',
    components: {VueDatePicker},
    props: ['project_id', 'patient_id', 'form_id', 'submission_id'],
    data() {
        return {
            project: undefined,
            patient: undefined,
            form: undefined,
            answers: {},
            error: "",
            submission: undefined
        }
    },
    methods: {
        formatDateTime,
        back: function () {
            this.$router.back()
        },
        save: async function () {
            try {
                await this.submission.save()
                let submissions = (await this.patient.submissions)
                submissions.push(this.submission)
                this.back()
            } catch (e) {
                this.error = e.message
            }
        },

        getInputType: function (field) {
            if (field.type === 'string') {
                return 'text'
            }
            if (field.type === 'integer') {
                return 'number'
            }
            if (field.type === 'float') {
                return 'number'
            }
        }
    },
    computed: {
        disabled: function () {
            return this.submission_id
        }
    },
    async mounted() {
        this.project = this.state.user.projects.find(project => {
            return project.id === parseInt(this.project_id)
        })

        this.patient = (await this.project.patients).find(patient => patient.id === parseInt(this.patient_id))

        if (this.submission_id) {
            this.submission = (await this.patient.submissions).find(submission => submission.id === parseInt(this.submission_id))
            this.form = this.project.forms.find(form => form.id === this.submission.form_id)
        } else if (this.form_id) {
            this.form = this.project.forms.find(form => form.id === parseInt(this.form_id))
            this.submission = Submission.create(this.project_id, this.patient_id, this.form_id)
        }

    }
}
</script>

<style scoped>
.col-form-label.required:after {
    content: " *";
    color: red;
}
</style>
