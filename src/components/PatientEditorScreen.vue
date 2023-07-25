<template>
    <div v-if="project && patient">
        <h4 class="my-3" v-if="!patient.id">Добавление пациента в проект "{{ project.name }}"</h4>
        <h4 class="my-3" v-if="patient.id">Изменение данных пациента "{{ patient.name }}"</h4>

        <div class="alert alert-warning" v-if="error">
            {{ error }}
        </div>

        <form>
            <div class="mb-3">
                <label class="form-label">ФИО</label>
                <input type="text" class="form-control" v-model="patient.name">
            </div>

            <div class="mb-3">
                <label class="form-label">Дата рождения</label>
                <VueDatePicker auto-apply model-type="yyyy-MM-dd" v-model="patient.birthday"
                               input-class-name="form-control" text-input
                               :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                               select-text="Выбрать" cancel-text="Закрыть" required/>
            </div>

            <div class="mb-3">
                <label class="form-label">Пол</label>
                <select class="form-control" v-model="patient.sex">
                    <option value="male">Мужской</option>
                    <option value="female">Женский</option>
                </select>
            </div>

            <div class="mb-3" v-if="can_create_medsenger_contract">
                <div class="form-check form-switch">
                    <input class="form-check-input" role="switch" type="checkbox"
                           v-model="patient.medsenger_contract"
                           :disabled="patient && patient.contract_id != null">
                    <label class="form-label">Создать контракт в Medsenger</label>
                </div>
            </div>

            <div class="mb-3" v-if="patient.medsenger_contract && (!patient || patient.contract_id == null)">
                <label class="form-label">Email</label>
                <input type="text" class="form-control" v-model="patient.email">
            </div>

            <div class="mb-3" v-if="patient.medsenger_contract && (!patient || patient.contract_id == null)">
                <label class="form-label">Длительность</label>
                <select class="form-control" v-model="patient.days">
                    <option :value="180">180 дней</option>
                </select>
            </div>

            <a v-if="!patient" @click="save" class="btn btn-primary">Добавить</a>
            <a v-if="patient" @click="save" class="btn btn-primary">Сохранить</a>
            <a @click="back()" class="btn btn-warning ms-1">Назад</a>
        </form>
    </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Patient from "@/models/Patient";

export default {
    name: 'PatientEditorScreen',
    components: {VueDatePicker},
    props: ['project_id', 'id'],
    data() {
        return {
            project: undefined,
            error: '',
            patient: undefined,
            can_create_medsenger_contract: process.env.VUE_APP_MEDSENGER_CONTRACTS
        }
    },
    methods: {
        save: async function (e) {
            e.preventDefault();
            try {
                if (this.patient.id) {
                    await this.patient.save()
                } else {
                    await this.patient.save()
                    let patients = await this.project.patients
                    patients.push(this.patient)
                }

                this.$router.back()
            } catch (e) {
                this.error = e.message
            }
        },
        back: function () {
            if (this.patient.id) {
                this.patient.reset()
            }
            this.$router.back()
        }
    },
    async mounted() {
        this.project = this.state.user.projects.find(project => {
            console.log(project);
            return project.id === parseInt(this.project_id)
        })

        if (this.id) {
            this.patient = (await this.project.patients).find(patient => patient.id === parseInt(this.id))
        } else {
            this.patient = new Patient(this.project_id)
        }

    }
}
</script>

<style scoped>

</style>
