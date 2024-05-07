<template>
    <div v-if="project && patient && form && submission">

        <div @drop="onDrop" @dragenter="dragEnter" @dragleave="dragLeave" :class="{'bordered': has_border}"
             @dragover="dragOver">
            <div class="description">
                <div class="hstack gap-3">
                    <div class="me-auto">
                        <h4 class="my-3">{{ patient.name }}: {{ form.name }} <small
                            v-if="this.disabled"> ({{ this.submission.readable_created_on }} / {{
                                this.submission.author
                            }})</small></h4>
                    </div>
                    <div class="no-print">
                        <button onclick="window.print()"
                                class="btn btn-primary btn-sm me-1 my-1">Печать
                        </button>
                        <button
                            @click="$router.push({name: 'form_compare', params: {project_id: project.id, patient_id: patient.id, form_id: form.id}})"
                            class="btn btn-primary btn-sm me-1 my-1">Сравнение
                        </button>
                        <button @click="edit()" v-if="disabled && !editing"
                                class="btn btn-primary btn-sm me-1 my-1">Изменить
                        </button>

                        <a v-if="state.user && state.user.is('администратор') && disabled"
                           class="btn btn-sm btn-danger me-1 my-1"
                           @click="delete_submission()">Удалить форму</a>

                        <button @click="back()" class="btn btn-warning btn-sm me-1 my-1">Назад</button>
                    </div>
                </div>

                <p class="no-print">{{ form.description }}</p>

            </div>

            <div class="alert alert-warning" v-if="error">
                {{ error }}
            </div>

            <div v-for="part in form.parts" v-bind:key="part.id">
                <div class="card mb-2" v-if="part.repeatable && !disabled">
                    <div class="card-body">
                        <div class="hstack gap-3">
                            <div><h5 class="card-title my-0">{{ part.name }}</h5></div>
                            <div class="text-muted no-print"><small>{{ part.description }}</small></div>
                            <div class="ms-auto">
                                <button class="btn btn-primary btn-sm" @click="submission.extend(part)">Добавить
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card" :class="{'my-3': !part.repeatable, 'mb-2 bg-light': part.repeatable }"
                     v-for="(group, group_key) in submission.answers[part.id]" v-bind:key="group_key">
                    <div class="card-body">
                        <div class="hstack gap-3 mb-3">
                            <div><h6 v-if="part.repeatable" class="card-title my-0">{{ part.name }}</h6><h5 v-else
                                                                                                            class="card-title my-0">
                                {{ part.name }}</h5></div>
                            <div><small v-if="!part.repeatable" class="text-muted no-print">{{
                                    part.description
                                }}</small></div>
                            <div class="ms-auto" v-if="part.repeatable && !disabled">
                                <button class="btn btn-warning btn-sm" @click="submission.remove(part, group_key)">
                                    Удалить
                                </button>
                            </div>
                        </div>

                        <div v-for="field in part.fields" v-bind:key="field.id">
                            <div v-if="field.type === 'subheader'"><h6 class="my-3">{{ field.text }}</h6></div>
                            <div v-else>
                                <div class="row mb-3"
                                     v-if="!field.show_if || submission.answers[part.id][group_key][field.show_if]"
                                     :class="{'no-print': !submission.answers[part.id][group_key][field.id]}">
                                    <label class="col-sm-4 col-form-label" :class="{ required: field.required }">{{
                                            field.text
                                        }}</label>

                                    <div class="col-sm-8" :ref="part.id + '_' + group_key + '_' + field.id">
                                        <input
                                            :class="{'is-invalid': searchForArray(error_fields, [part.id, group_key, field.id])}"
                                            v-if="field.type === 'string'" type="text" class="form-control no-print"
                                            v-model="submission.answers[part.id][group_key][field.id]"
                                            v-bind:required="field.required" v-bind:disabled="disabled">

                                        <input
                                            :class="{'is-invalid': searchForArray(error_fields, [part.id, group_key, field.id])}"
                                            v-if="field.type === 'integer'" type="number" step="1"
                                            class="form-control no-print"
                                            v-model="submission.answers[part.id][group_key][field.id]"
                                            v-bind:required="field.required" v-bind:disabled="disabled">

                                        <input
                                            :class="{'is-invalid': searchForArray(error_fields, [part.id, group_key, field.id])}"
                                            v-if="field.type === 'float'" type="number" step="0.01"
                                            class="form-control no-print"
                                            v-model="submission.answers[part.id][group_key][field.id]"
                                            v-bind:required="field.required" v-bind:disabled="disabled">

                                        <textarea
                                            :class="{'is-invalid': searchForArray(error_fields, [part.id, group_key, field.id])}"
                                            v-if="field.type === 'text'" class="form-control no-print"
                                            v-model="submission.answers[part.id][group_key][field.id]"
                                            v-bind:required="field.required" v-bind:disabled="disabled"></textarea>

                                        <div class="col-sm-8 only-print" style="padding-top: 7px;"
                                             v-if="['string', 'text', 'float', 'integer'].includes(field.type)">
                                            <p style=" margin-bottom: 0;">
                                                {{ submission.answers[part.id][group_key][field.id] }}
                                            </p>
                                        </div>

                                        <VueDatePicker v-if="field.type === 'date'" auto-apply model-type="yyyy-MM-dd"
                                                       v-model="submission.answers[part.id][group_key][field.id]"
                                                       :input-class-name="className(part.id, group_key, field.id)"
                                                       text-input
                                                       :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                                                       select-text="Выбрать" cancel-text="Закрыть"
                                                       v-bind:required="field.required"
                                                       v-bind:disabled="disabled"/>

                                        <div v-if="['radio', 'select'].includes(field.type) && disabled && !Object.keys(field.params.options).includes(submission.answers[part.id][group_key][field.id])">
                                            <p>{{ submission.answers[part.id][group_key][field.id] }}</p>
                                        </div>
                                        <div v-else>
                                            <div v-if="field.type === 'radio'">
                                            <div v-for="(value, option) in field.params.options"
                                                 v-bind:key='option'
                                                 class="form-check">
                                                <input class="form-check-input" type="radio"
                                                       :value="fillPatientData(value, this.patient)"
                                                       v-model="submission.answers[part.id][group_key][field.id]"
                                                       v-bind:disabled="disabled">
                                                <label class="form-check-label">
                                                    {{ fillPatientData(option, this.patient) }}
                                                </label>
                                            </div>
                                        </div>

                                        <div v-if="field.type === 'select'">
                                            <select class="form-control form-select"
                                                    :class="{'is-invalid': searchForArray(error_fields, [part.id, group_key, field.id])}"
                                                    v-model="submission.answers[part.id][group_key][field.id]"
                                                    v-bind:disabled="disabled">
                                                <option v-for="(value, option) in field.params.options" :value="value"
                                                        :key="value">{{ option }}
                                                </option>
                                            </select>
                                        </div>
                                        </div>


                                        <div class="form-check" v-if="field.type === 'checkbox'">
                                            <input class="form-check-input" type="checkbox"
                                                   v-model="submission.answers[part.id][group_key][field.id]"
                                                   v-bind:disabled="disabled">
                                        </div>

                                        <div class="form-text no-print" v-if="field.description">{{
                                                field.description
                                            }}
                                        </div>
                                        <hr style="margin: 0.7rem 0; border-top: 1px dotted;" class="only-print">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <hr class="no-print" style="border-top: dotted 1px;"/>
            </div>
        </div>
    </div>

    <div class="alert alert-warning" v-if="error">
        {{ error }}
    </div>

    <div class="my-3 no-print">
        <loading-button @click="save()" class_name="btn btn-primary" v-if="!disabled">Сохранить</loading-button>
        <button @click="back()" class="btn btn-warning mx-1">Назад</button>
    </div>


</template>

<script>

import VueDatePicker from "@vuepic/vue-datepicker";
import {fillPatientData, formatDateTime, searchForArray} from "../utils/helpers";
import Submission from "@/models/Submission";
import LoadingButton from "@/components/parts/common/LoadingButton.vue";
import * as XLSX from "xlsx";

export default {
    name: 'FormScreen',
    components: {LoadingButton, VueDatePicker},
    props: ['project_id', 'patient_id', 'form_id', 'submission_id'],
    data() {
        return {
            project: undefined,
            patient: undefined,
            form: undefined,
            answers: {},
            error: "",
            error_fields: [],
            submission: undefined,
            editing: false,
            drag_counter: 0
        }
    },
    methods: {
        fillPatientData,
        searchForArray,
        formatDateTime,
        dragEnter: function () {
            this.drag_counter += 1
            console.log('drag enter', this.drag_counter)
        },
        dragLeave: function () {
            this.drag_counter -= 1
            console.log('drag leave', this.drag_counter)
        },
        dragOver: function (e) {
            e.stopPropagation();
            e.preventDefault();
        },
        save: async function () {
            this.error_fields = []

            try {
                await this.submission.save()
                await this.patient.refresh()
                this.editing = false
                this.back()
            } catch (e) {
                console.log(e)
                this.error = e.message
                this.error_fields = e.details

                if (this.error_fields.length > 0) {
                    let first_error = this.error_fields[0]
                    this.$refs[first_error[0] + '_' + first_error[1] + '_' + first_error[2]][0].scrollIntoView({ behavior: 'smooth' });
                }
            }
        },
        edit: function () {
            this.editing = true
            this.enableExitWarning()
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
        },
        className: function (part_id, group_key, field_id) {
            if (searchForArray(this.error_fields, [part_id, group_key, field_id])) {
                return "form-control is-invalid"
            } else {
                return "form-control"
            }
        },
        back: function () {
            this.disableExitWarning()
            if (this.submission_id && this.editing) {
                this.submission.reset()
            }
            this.$router.back()
        },
        delete_submission: async function () {
            if (confirm("Вы точно хотите удалить форму " + this.form.name + " для пациента " + this.patient.name + "?")) {
                await this.submission.delete()
                await this.patient.refresh()
                this.$router.push({name: 'patient', params: {project_id: this.project.id, id: this.patient.id}})
            }
        },
        onDrop: async function (e) {
            e.stopPropagation()
            e.preventDefault()
            this.drag_counter = 0
            let data = await e.dataTransfer.files[0].arrayBuffer()
            const workbook = XLSX.read(data);
            const worksheet = workbook.Sheets[workbook.SheetNames[0]];
            const raw_data = XLSX.utils.sheet_to_json(worksheet, {header: 1});

            console.log(raw_data)

            const answers = {}

            raw_data.forEach(row => {
                if (row.length > 8 && row[1] && row[8] !== undefined) {
                    answers[row[1].trim()] = row[8]
                }
            })

            console.log(answers)

            if (!this.id || this.editing) {
                this.submission.import(answers)
            }
        },
        exitWarning: function (event) {
            // Recommended
            event.preventDefault();

            // Included for legacy support, e.g. Chrome/Edge < 119
            event.returnValue = true;
        },
        enableExitWarning: function () {
            window.addEventListener("beforeunload", this.exitWarning);
        },
        disableExitWarning: function () {
            window.removeEventListener("beforeunload", this.exitWarning);
        }
    },
    computed: {
        disabled: function () {
            return this.submission_id && !this.editing
        },
        has_border: function () {
            return this.drag_counter > 0
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
            this.enableExitWarning()
            this.form = this.project.forms.find(form => form.id === parseInt(this.form_id))
            this.submission = Submission.create(this.project, this.patient, this.form)
        }

    }
}
</script>

<style scoped>
.col-form-label.required:after {
    content: " *";
    color: red;
}

.bordered {
    border: 1px dotted gray !important;
}

.form-control:disabled {
    background-color: #fafafa;
}

.form-select:disabled {
    background-color: #fafafa;
}

.dp__disabled {
    background-color: #fafafa;
}
</style>
