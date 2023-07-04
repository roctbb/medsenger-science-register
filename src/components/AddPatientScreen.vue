<template>
    <div v-if="project">
        <h4 class="my-3">Добавление пациента в проект "{{ project.name }}"</h4>

        <div class="alert alert-warning" v-if="error">
            {{ error }}
        </div>

        <form>
            <div class="mb-3">
                <label class="form-label">ФИО</label>
                <input type="text" class="form-control" v-model="newPatient.name">
            </div>

            <div class="mb-3">
                <label class="form-label">Дата рождения</label>
                <VueDatePicker auto-apply model-type="yyyy-MM-dd" v-model="newPatient.birthday"
                               input-class-name="form-control" text-input
                               :enable-time-picker="false" locale="ru-RU" format="dd.MM.yyyy"
                               select-text="Выбрать" cancel-text="Закрыть" required/>
            </div>

            <div class="mb-3">
                <label class="form-label">Пол</label>
                <select class="form-control" v-model="newPatient.sex">
                    <option value="male">Мужской</option>
                    <option value="female">Женский</option>
                </select>
            </div>

            <button @click="addPatient" class="btn btn-primary">Добавить</button>
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
            newPatient: undefined
        }
    },
    methods: {
        addPatient: async function (e) {
            e.preventDefault();
            try {
                await this.managers.project.addPatient(this.project, this.newPatient)
            } catch (e) {
                this.error = e.message
            }
        },
        clear: function () {
            this.newPatient = {
                name: '',
                sex: 'male',
                birthday: ''
            }
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

        this.clear()
    }
}
</script>

<style scoped>

</style>
