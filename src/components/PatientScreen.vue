<template>
    <div v-if="project && patient">

        <div class="hstack gap-3">
            <div class="me-auto my-3">
                <h4 class="my-1">{{ patient.name }} <small class="text-muted">пациент ID {{ patient.id }}</small><small
                    class="text-muted"
                    v-if="patient.step">
                    / {{ patient.step }}</small></h4>
            </div>
            <div>
                <a @click="$router.push({name: 'project', params: {id: this.project.id}})"
                   class="btn btn-warning btn-sm me-1 my-1">Назад
                </a>
                <a target="_blank" class="btn btn-sm btn-success me-1 my-1" v-if="patient.contract_id"
                   :href="medsenger_host + '/client#/?c=' + patient.contract_id">Medsenger</a>
                <a class="btn btn-sm btn-success me-1 my-1"
                   @click="$router.push({name: 'edit_patient', params: {project_id: this.project.id, id: this.patient.id}})">Изменить
                    профиль</a>

                <a v-if="state.user.is('администратор')" class="btn btn-sm btn-danger me-1 my-1"
                   @click="delete_patient()">Удалить пациента</a>
            </div>
        </div>

        <div class="row my-1">
            <div class="col">
                <input type="text" placeholder="Поиск..." v-model="search_field" class="form-control"/>
            </div>
        </div>

        <p class="text-muted my-3">{{ patient.readable_birthday }} <span
            v-if="patient.phone"> / телефон {{ patient.phone }}</span><span v-if="patient.created_by"> / добавлен врачом {{
                patient.created_by
            }}</span></p>

        <div class="row" v-if="submissions">
            <div
                :class="{'col-12': !project.settings.show_files && !project.settings.show_comments, 'col-8': project.settings.show_files || project.settings.show_comments}">
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

                                    <div v-for="pair in submission.show_off_fields()" :key="pair">
                                        <small class="text-muted my-0">{{ pair.title }}: {{ pair.value }}</small>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <p class="mb-3" v-if="!apply_search(submissions, group).length"><small>Нет данных</small></p>
                    </div>

                    <div>
                        <button class="btn btn-primary btn-sm mb-4" type="button"
                                data-bs-toggle="modal" :data-bs-target="`#group_${group.id}`"
                                aria-expanded="false">
                            Добавить
                        </button>

                        <div class="modal fade" :id="`group_${group.id}`" tabindex="-1"
                             :aria-labelledby="`group_${group.id}Label`" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-scrollable modal-dialog-centered modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" :id="`group_${group.id}Label`">{{ group.name }}</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                aria-label="Закрыть"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="d-grid gap-2">
                                            <button v-for="form in available_forms(group)" v-bind:key="form.id"
                                                    class="btn btn-light text-start" data-bs-dismiss="modal"
                                                    @click="$router.push({name: 'form', params: {project_id: project.id, patient_id: patient.id, form_id: form.id}})">
                                                {{
                                                    form.name
                                                }}
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-4" style="border-left: 1px dotted gray;"
                 v-if="project.settings.show_files || project.settings.show_comments">

                <div v-if="project.settings.show_files">
                    <h6>Дополнительные документы по пациенту</h6>

                    <div v-if="files && files.length" class="my-3">
                        <ul>
                            <li v-for="file in files" :key="'file_' + file.id">
                                <button class="btn btn-link btn-sm text-left" @click="download_file(file)">
                                    {{ file.name }} (скачать)
                                </button>
                                <font-awesome-icon v-if="state.user.has_permission(file.doctor_id)"
                                                   :icon="['fas', 'times']"
                                                   @click="delete_file(file)"/>
                            </li>
                        </ul>
                    </div>
                    <div v-else class="my-3">
                        <small>Нет документов</small>
                    </div>


                    <p class="my-2"><strong><small>Добавить документ</small></strong></p>
                    <div class="mb-2">
                        <input type="email" class="form-control form-control-sm" id="fileName"
                               placeholder="Название документа" v-model="new_file.name">
                    </div>
                    <div class="mb-2">
                        <input class="form-control form-control-sm" type="file" id="formFile" ref="formFile"
                               @change="change_file">
                    </div>
                    <button @click="upload_file"
                            class="btn btn-success btn-sm me-1 my-1">Загрузить документ
                    </button>
                    <div class="alert alert-warning" v-if="file_error">
                        {{ file_error }}
                    </div>

                </div>

                <div v-if="project.settings.show_comments">

                    <h6 class="mb-1 mt-5">Комментарии по статусу пациента</h6>

                    <p class="my-3" v-for="comment in patient.comments" :key="comment.id"><small><strong>{{
                            comment.author
                        }}</strong><span v-if="comment.description"> / {{ comment.description }}</span>: {{
                            comment.text
                        }}</small><br><small
                        class="text-muted">{{ comment.readable_created_on }}</small>
                    </p>
                    <p class="my-3" v-if="!patient.comments.length"><small>Комментариев еще нет</small></p>

                    <textarea class="form-control" v-model="new_comment"></textarea>
                    <button @click="addComment()" class="btn btn-sm btn-success my-2">Добавить</button>
                </div>
            </div>
        </div>
        <loading v-else></loading>


    </div>
    <loading v-else></loading>
</template>

<script>

import {empty, formatDate, formatDateTime, toBase64} from "../utils/helpers";
import Loading from "@/components/Loading.vue";
import PatientFile from "@/models/PatientFile";

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
            new_comment: "",
            files: [],
            new_file: {name: ''},
            file_error: undefined,
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
        },
        upload_file: function () {
            let file_to_upload = PatientFile.create(this.project, this.patient, this.new_file)
            file_to_upload.save().then(() => {
                this.files.push(file_to_upload)
                this.new_file = {name: ''}
                this.$refs.formFile.value = null;
            }).catch((e) => {
                console.log(e)
                this.file_error = e.message
            })
        },
        download_file: function (file) {
            file.download()
        },
        delete_file: function (file) {
            if (confirm("Удалить файл " + file.name + "?")) {
                file.delete().then(() => {
                    this.files = this.files.filter((f) => f.id != file.id)
                })
            }
        },
        change_file: function (event) {
            let file = event.target.files[0]
            if (file.size > 50 * 1024 * 1024) {
                // this.file_states.push('<strong>' + file.name + ':</strong> Размер файла не должен превышать 50 МБ.')
            } else {
                this.new_file.file_name = file.name
                this.new_file.size = file.size
                this.new_file.type = file.type ?? 'text/plain'

                toBase64(file).then((base64) => {
                    this.new_file.base64 = base64
                })
            }
        },
        delete_patient: async function () {
            if (confirm("Вы точно хотите удалить пациента " + this.patient.name + "?")) {
                await this.patient.delete()
                await this.project.refresh()
                this.$router.push({name: 'project', params: {id: this.project.id}})
            }
        }
    },
    async mounted() {
        if (this.state.user) {
            this.project = this.state.user.projects.find(project => {
                console.log(project);
                return project.id === parseInt(this.project_id)
            })

            this.patient = (await this.project.patients).find(patient => patient.id === parseInt(this.id))
            this.submissions = await this.patient.submissions
            this.files = await this.patient.files
        }

    }
}
</script>

<style scoped>

</style>
