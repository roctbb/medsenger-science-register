<template>
    <div v-if="project">
        <h4 class="my-3" v-if="!patient">Добавление пациента в проект "{{ project.name }}"</h4>
        <h4 class="my-3" v-if="patient">Изменение данных пациента "{{ patient.name }}"</h4>

        <div class="alert alert-warning" v-if="error">
            {{ error }}
        </div>

        <form>
            <div class="mb-3">
                <label class="form-label">ФИО</label>
                <input type="text" class="form-control" v-model="editedPatient.name">
            </div>

            <div class="mb-3">
                <label class="form-label">Дата рождения</label>
                <VueDatePicker auto-apply model-type="yyyy-MM-dd" v-model="editedPatient.birthday"
                               input-class-name="form-control" text-input
                               :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                               select-text="Выбрать" cancel-text="Закрыть" required/>
            </div>

            <div class="mb-3">
                <label class="form-label">Пол</label>
                <select class="form-control" v-model="editedPatient.sex">
                    <option value="male">Мужской</option>
                    <option value="female">Женский</option>
                </select>
            </div>

            <button v-if="!patient" @click="save" class="btn btn-primary">Добавить</button>
            <button v-if="patient" @click="save" class="btn btn-primary">Сохранить</button>
            <button @click="back()" class="btn btn-warning ms-1">Назад</button>
        </form>
    </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

export default {
    name: 'AddPatientScreen',
    components: {VueDatePicker},
    data() {
        return {
            project: undefined,
            error: '',
            editedPatient: undefined,
            patient: undefined
        }
    },
    methods: {
        save: async function (e) {
            e.preventDefault();
            try {
                await this.managers.project.storePatient(this.project, this.editedPatient)
                this.clear()
            } catch (e) {
                this.error = e.message
            }
        },
        clear: function () {
            this.editedPatient = {
                name: '',
                sex: 'male',
                birthday: '',
                id: undefined
            }
            this.error = ''
            this.patient = undefined
        },
        back: function () {
            this.clear()
            this.managers.project.open(this.project)
        }
    },
    mounted() {
        this.event_bus.on('project-selected', (project) => {
            this.project = project
        });

        this.event_bus.on('patient-selected', (patient) => {
            this.patient = patient
            this.editedPatient = {
                name: patient.name,
                sex: patient.sex,
                birthday: patient.birthday,
                id: patient.id
            }
        });

        this.event_bus.on('clear-patient', () => {
            this.clear()
        });

        this.clear()
    }
}
</script>

<style scoped>

</style>
