<template>
    <div v-if="project && patient && form && submissions">

        <div class="description">
            <div class="hstack gap-3">
                <div class="me-auto">
                    <h4 class="my-3">{{ patient.name }}: {{ form.name }} </h4>
                </div>
                <div>
                    <button onclick="window.print()"
                            class="btn btn-primary btn-sm me-1">Печать
                    </button>
                    <button @click="edit()" v-if="disabled && !editing"
                            class="btn btn-primary btn-sm me-1">Изменить
                    </button>
                </div>
            </div>

            <p>{{ form.description }}</p>

        </div>

        <div class="alert alert-warning" v-if="error">
            {{ error }}
        </div>

        <div v-for="part in form.parts" v-bind:key="part.id">
            <div class="card">
                <div class="card-body">
                    <table class="table table-striped" v-for="row in extractParts(submissions, part)"
                           :key="row">
                        <thead>
                            <tr><th>{{ part.name }}</th><td v-for="submission in submissions" :key="submission.id">{{ submission.readable_created_on }}</td></tr>
                        </thead>
                        <tbody>
                        <tr v-for="field in part.fields" v-bind:key="field.id">
                            <td>
                                <div><strong>{{ field.text }}</strong></div>
                                <div class="form-text" v-if="field.description">{{ field.description }}</div>
                            </td>
                            <td v-for="(submission_answers, i) in row" :key="i">
                                <input
                                    v-if="field.type === 'string'" type="text" class="form-control"
                                    v-model="submission_answers[field.id]"
                                    v-bind:required="field.required" disabled>

                                <input
                                    v-if="field.type === 'integer'" type="number" step="1" class="form-control"
                                    v-model="submission_answers[field.id]"
                                    v-bind:required="field.required" disabled>

                                <input
                                    v-if="field.type === 'float'" type="number" step="0.01" class="form-control"
                                    v-model="submission_answers[field.id]"
                                    v-bind:required="field.required" disabled>

                                <textarea
                                    v-if="field.type === 'text'" class="form-control"
                                    v-model="submission_answers[field.id]"
                                    v-bind:required="field.required" disabled></textarea>


                                <VueDatePicker v-if="field.type === 'date'" auto-apply model-type="yyyy-MM-dd"
                                               v-model="submission_answers[field.id]"
                                               text-input
                                               :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                                               select-text="Выбрать" cancel-text="Закрыть"
                                               v-bind:required="field.required"
                                               disabled/>

                                <div v-if="field.type === 'radio'">
                                    <div v-for="(value, option) in field.params.options"
                                         v-bind:key='option'
                                         class="form-check">
                                        <input class="form-check-input" type="radio"
                                               :value="value"
                                               v-model="submission_answers[field.id]"
                                               disabled>
                                        <label class="form-check-label">
                                            {{ option }}
                                        </label>
                                    </div>
                                </div>

                                <div v-if="field.type === 'select'">
                                    <select class="form-control form-select"
                                            v-model="submission_answers[field.id]"
                                            disabled>
                                        <option v-for="(value, option) in field.params.options" :value="value"
                                                :key="value">{{ option }}
                                        </option>
                                    </select>
                                </div>

                                <div class="form-check" v-if="field.type === 'checkbox'">
                                    <input class="form-check-input" type="checkbox"
                                           v-model="submission_answers[field.id]"
                                           disabled>
                                </div>
                            </td>
                        </tr>
                        </tbody>


                    </table>

                </div>

            </div>

        </div>

        <div class="my-3 no-print">
            <button @click="save()" class="btn btn-primary" v-if="!disabled">Сохранить</button>
            <button @click="back()" class="btn btn-warning mx-1">Назад</button>
        </div>

    </div>
</template>

<script>

import VueDatePicker from "@vuepic/vue-datepicker";
import {formatDateTime, searchForArray} from "../utils/helpers";

export default {
    name: 'FormScreen',
    components: {VueDatePicker},
    props: ['project_id', 'patient_id', 'form_id', 'submission_id'],
    data() {
        return {
            project: undefined,
            patient: undefined,
            form: undefined,
            submissions: undefined
        }
    },
    methods: {
        searchForArray,
        formatDateTime,
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
        },
        back: function () {
            this.$router.back()
        },
        extractParts: function (submissions, form_part) {
            let max_length = 0

            submissions.forEach(s => {
                let sa = s.answers
                if (sa[form_part.id]) {
                    if (Object.keys(sa[form_part.id]).length > max_length) {
                        max_length = Object.keys(sa[form_part.id]).length
                    }
                }
            })

            const getPart = (s, i) => {
                let sp = s.answers[form_part.id]
                if (Object.keys(sp).length > i) {
                    return sp[Object.keys(sp).at(i)]
                } else {
                    return null
                }
            }

            let parts = []
            for (let i = 0; i < max_length; i++) {
                let row = []
                submissions.forEach(s => {
                    console.log(getPart(s, i))
                    row.push(getPart(s, i))
                })
                parts.push(row)
            }
            return parts
        }
    },
    computed: {
        disabled: function () {
            return this.submission_id && !this.editing
        }
    },
    async mounted() {
        this.project = this.state.user.projects.find(project => {
            return project.id === parseInt(this.project_id)
        })

        this.patient = (await this.project.patients).find(patient => patient.id === parseInt(this.patient_id))
        this.form = this.project.forms.find(form => form.id === parseInt(this.form_id))
        this.submissions = (await this.patient.submissions).filter(s => s.form_id === parseInt(this.form_id))
    }
}
</script>

<style scoped>

</style>
