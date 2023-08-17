<template>
    <div v-if="project && patient">

        <div class="hstack gap-3">
            <div class="me-auto my-3">
                <h4 class="my-1">{{ patient.name }} <small class="text-muted">пациент</small><small class="text-muted" v-if="patient.step"> / {{ patient.step }}</small></h4>
            </div>
            <div>
                <button @click="$router.push({name: 'project', params: {id: this.project.id}})"
                        class="btn btn-warning btn-sm me-1">Назад
                </button>
                <a target="_blank" class="btn btn-sm btn-success me-1" v-if="patient.contract_id"
                   :href="medsenger_host + '/client#/?c=' + patient.contract_id">Medsenger</a>
                <a class="btn btn-sm btn-success me-1"
                   @click="$router.push({name: 'edit_patient', params: {project_id: this.project.id, id: this.patient.id}})">Изменить
                    профиль</a>
            </div>
        </div>

        <div class="row my-1">
            <div class="col">
                <input type="text" placeholder="Поиск..." v-model="search_field" class="form-control"/>
            </div>
        </div>

        <p class="text-muted my-3">{{ patient.readable_birthday }} <span
            v-if="patient.phone"> / телефон {{ patient.phone }}</span></p>

        <div class="row" v-if="submissions">
            <div class="col-8">
                <div v-for="group in project.form_groups" :key="group.id">
                    <h6 class="mb-2" v-if="project.form_groups.length > 1">{{ group.name }}</h6>
                    <div class="row pt-2">
                        <div class="col col-sm-6 col-md-4 col-lg-3 mb-3"
                             v-for="submission in apply_search(submissions, group)"
                             v-bind:key="submission.id">
                            <div class="card"
                                 @click="$router.push({name: 'submission', params: {project_id: project.id, patient_id: patient.id, submission_id: submission.id}})">
                                <div class="card-body">
                                    <h6 class="card-title">{{ submission.form.name }}</h6>
                                    <small class="text-muted my-0">{{ submission.readable_created_on }}</small><br>
                                    <small class="text-muted my-0">{{ submission.author }}</small>
                                </div>
                            </div>
                        </div>

                        <p class="mb-3" v-if="!apply_search(submissions, group).length"><small>Нет данных</small></p>
                    </div>

                    <div class="dropdown d-inline">
                        <button class="btn btn-primary btn-sm dropdown-toggle mb-4" type="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false">
                            Добавить
                        </button>

                        <ul class="dropdown-menu">
                            <li v-for="form in available_forms(group)" v-bind:key="form.id"><a
                                class="dropdown-item text-wrap"
                                @click="$router.push({name: 'form', params: {project_id: project.id, patient_id: patient.id, form_id: form.id}})">{{
                                    form.name
                                }}</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-4" style="border-left: 1px dotted gray;">
                <h6 class="mb-2">Комментарии</h6>

                <p class="my-3" v-for="comment in patient.comments" :key="comment.id"><small><strong>{{
                        comment.author
                    }}</strong><span v-if="comment.description"> / {{ comment.description }}</span>: {{ comment.text }}</small><br><small class="text-muted">{{ comment.readable_created_on }}</small>
                </p>
                <p class="my-3" v-if="!patient.comments.length"><small>Комментариев еще нет</small></p>

                <textarea class="form-control" v-model="new_comment"></textarea>
                <button @click="addComment()" class="btn btn-sm btn-success my-2">Добавить</button>
            </div>
        </div>
        <loading v-else></loading>


    </div>
    <loading v-else></loading>
</template>

<script>

import {empty, formatDate, formatDateTime} from "../utils/helpers";
import Loading from "@/components/Loading.vue";

export default {
    name: 'PatientScreen',
    props: ['project_id', 'id'],
    components: {Loading},
    data() {
        return {
            project: undefined,
            patient: undefined,
            search_field: "",
            submissions: undefined,
            medsenger_host: process.env.VUE_APP_MEDSENGER_HOST,
            new_comment: ""
        }
    },
    methods: {
        formatDateTime,
        formatDate,
        available_forms: function (category) {
            if (category === undefined || this.project.form_groups.length < 2) {
                return this.project.forms.filter(form => !form.specialty || this.state.user.is(form.specialty))
            } else {
                return this.project.forms.filter(form => form.category_id === category.id && (!form.specialty || this.state.user.is(form.specialty)))
            }
        },
        apply_search: function (submissions, group) {
            let query = this.search_field.toLowerCase()

            let filtered_submissions = submissions.filter(s => this.project.form_groups.length < 2 || s.form.category_id === group.id).filter(s =>
                empty(this.search_field) ||
                s.form.name.toLowerCase().includes(query) ||
                s.readable_created_on.includes(query) ||
                s.author.toLowerCase().includes(query)
            )

            filtered_submissions.sort((a, b) => a.created_on - b.created_on)
            return filtered_submissions
        },
        addComment: function () {
            this.patient.add_comment(this.new_comment)
            this.new_comment = ""
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
