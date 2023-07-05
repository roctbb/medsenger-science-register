<template>
    <div v-if="project && patient && form">

        <h4 class="my-3">{{ patient.name }}: {{ form.name }} <small
            v-if="this.disabled"> ({{ formatDateTime(this.submission.created_on) }})</small></h4>

        <p>{{ form.description }}</p>

        <div class="alert alert-warning" v-if="error">
            {{ error }}
        </div>

        <div class="card" v-for="part in form.parts" v-bind:key="part.id">
            <div class="card-body">
                <h5 class="card-title">{{ part.name }}</h5>

                <div class="row mb-3" v-for="field in part.fields" v-bind:key="field.id">
                    <label class="col-sm-4 col-form-label" :class="{ required: field.required }">{{
                            field.text
                        }}</label>
                    <div class="col-sm-8">
                        <input v-if="field.type === 'string'" type="text" class="form-control"
                               v-model="answers[field.id]"
                               v-bind:required="field.required" v-bind:disabled="disabled">

                        <input v-if="field.type === 'integer'" type="number" step="1" class="form-control"
                               v-model="answers[field.id]"
                               v-bind:required="field.required" v-bind:disabled="disabled">

                        <input v-if="field.type === 'float'" type="number" step="0.01" class="form-control"
                               v-model="answers[field.id]"
                               v-bind:required="field.required" v-bind:disabled="disabled">

                        <textarea v-if="field.type === 'text'" class="form-control" v-model="answers[field.id]"
                                  v-bind:required="field.required" v-bind:disabled="disabled"></textarea>


                        <VueDatePicker v-if="field.type === 'date'" auto-apply model-type="yyyy-MM-dd"
                                       v-model="answers[field.id]"
                                       input-class-name="form-control" text-input
                                       :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                                       select-text="Выбрать" cancel-text="Закрыть" v-bind:required="field.required"
                                       v-bind:disabled="disabled"/>

                        <div v-if="field.type === 'radio'">
                            <div v-for="(value, option) in field.params.options"
                                 v-bind:key='option'
                                 class="form-check">
                                <input class="form-check-input" type="radio"
                                       :value="value" v-model="answers[field.id]" v-bind:disabled="disabled">
                                <label class="form-check-label">
                                    {{ option }}
                                </label>
                            </div>
                        </div>

                        <div class="form-check" v-if="field.type === 'checkbox'">
                            <input class="form-check-input" type="checkbox" v-model="answers[field.id]"
                                   v-bind:disabled="disabled">
                        </div>

                        <div class="form-text" v-if="field.description">{{ field.description }}</div>
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

export default {
    name: 'FormScreen',
    components: {VueDatePicker},
    data() {
        return {
            project: undefined,
            patient: undefined,
            form: undefined,
            answers: {},
            error: "",
            disabled: false,
            submission: undefined
        }
    },
    methods: {
        formatDateTime,
        back: function () {
            this.clear()
            this.managers.project.backToPatientPage()
        },
        save: async function () {
            try {
                await this.managers.submission.add(this.project, this.patient, this.form, this.answers)
                this.clear()
                this.back()
            } catch (e) {
                this.error = e.message
            }
        },
        clear: function () {
            this.answers = {}
            this.disabled = false
            this.submission = undefined
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
    mounted() {
        this.event_bus.on('project-selected', (project) => {
            this.project = project
        });

        this.event_bus.on('patient-selected', (patient) => {
            this.patient = patient
        });

        this.event_bus.on('form-selected', (form) => {
            this.form = form
        });

        this.event_bus.on('submission-selected', (submission) => {
            submission.records.forEach((record) => {
                this.answers[record.params.question_id] = record.value
            })
            this.disabled = true
            this.submission = submission
        });
    }
}
</script>

<style scoped>
.col-form-label.required:after {
    content: " *";
    color: red;
}
</style>
