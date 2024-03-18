<template>
    <div v-if="groups">
        <div>
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
    </div>
</template>

<script>


import {empty, formatDate} from "@/utils/helpers";

export default {
    name: 'PatientsCards',
    props: ['groups', 'project', 'search_field'],
    data() {
        return {
            table_enabled: false
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
}
</script>

<style scoped>

</style>
