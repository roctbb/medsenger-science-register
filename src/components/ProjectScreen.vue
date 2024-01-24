<template>
    <div v-if="project">
        <div class="hstack gap-3">
            <div class="me-auto">
                <h4 class="my-3">Список пациентов в проекте "{{ project.name }}"</h4>
                <p v-if="patients" class="my-2 text-muted">Пациентов в проекте: {{ patients.length }}</p>
            </div>
            <div>
                <button @click="$router.push({name: 'create_patient', params: {project_id: project.id}})"
                        class="btn btn-sm btn-primary me-1">Добавить
                </button>
                <a target="_blank" class="btn btn-sm btn-success me-1" href="https://telegynecology.ru/info/pat/47#libs">Материалы
                    для пациентов</a>
            </div>
        </div>

        <div class="row my-2" v-if="groups">
            <div class="col">
                <input type="text" placeholder="Поиск..." v-model="search_field" class="form-control"/>
            </div>
        </div>

        <div v-if="groups">
            <div class="row py-2" v-for="(group, i) in groups" :key="i">
                <h6 class="my-3" v-if="group.title"><span v-if="i !== groups.length - 1">Шаг {{
                        i + 1
                    }}. </span>{{ group.title }}</h6>

                <div class="col col-sm-6 col-md-4 col-lg-3 mb-3" v-for="patient in sortPatients(filterPatients(group))"
                     v-bind:key="patient.id">
                    <div class="card" :class="{'updated': patient.has_updates}">
                        <div class="card-body">
                            <div class="hstack">
                                <div class="me-auto"
                                     @click="$router.push({name: 'patient', params: {project_id: project.id, id: patient.id}})">
                                    <h6 class="card-title my-1">{{ patient.name }}</h6>
                                </div>
                                <div
                                    @click="$router.push({name: 'edit_patient', params: {project_id: this.project.id, id: patient.id}})">
                                    <font-awesome-icon :icon="['fas', 'pen']"/>
                                </div>
                            </div>

                            <small class="text-muted my-0">ID {{ patient.id }} / {{
                                    patient.readable_birthday
                                }}<br>{{ patient.created_by }}</small>

                            <div v-for="record in patient.show_off_records" :key="record">
                                <small class="text-muted my-0">{{ record.title }}: {{ record.value }}</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
        <loading v-else></loading>
    </div>
</template>

<script>


import {empty, formatDate} from "../utils/helpers";
import Loading from "@/components/Loading.vue";

export default {
    name: 'ProjectPatientsScreen',
    props: ['id'],
    components: {Loading},
    data() {
        return {
            search_field: '',
            patients: undefined,
            project: undefined,
            groups: undefined
        }
    },
    methods: {
        formatDate,
        sortPatients: function (patients) {
            patients.sort((a, b) => a.name.localeCompare(b.name))
            return patients
        },
        filterPatients: function (group) {
            return group.patients.filter((patient) => empty(this.search_field) || patient.name.toLowerCase().includes(this.search_field.toLowerCase()))
        }
    },
    async mounted() {
        if (this.state.user) {
            this.project = this.state.user.projects.find(project => {
                console.log(project);
                return project.id === parseInt(this.id)
            })
            this.patients = await this.project.patients
            this.groups = await this.project.groups
        }


    }
}
</script>

<style scoped>

</style>
