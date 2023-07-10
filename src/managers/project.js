import Manager from "@/managers/common";

class ProjectManager extends Manager {
    async getPatients(project) {
        return await this.api.project.getPatients(project.id)
    }

    open(project) {
        this.eventbus.emit('project-selected', project)
        this.eventbus.emit('change-screen', 'project-patients')
    }

    openPatientPage(patient) {
        this.eventbus.emit('patient-selected', patient)
        this.eventbus.emit('change-screen', 'patient')
    }

    backToPatientPage() {
        this.eventbus.emit('change-screen', 'patient')
    }

    addPatientPage() {
        this.eventbus.emit('clear-patient')
        this.eventbus.emit('change-screen', 'add-patient')
    }

    editPatientPage(patient) {
        this.eventbus.emit('patient-selected', patient)
        this.eventbus.emit('change-screen', 'add-patient')
    }

    async storePatient(project, patient) {
        if (!patient.id) {
            patient = await this.api.project.addPatient(project.id, patient.name, patient.sex, patient.birthday, patient.medsenger_contract, patient.email, patient.days)
        } else {
            patient = await this.api.project.editPatient(project.id, patient.id, patient.name, patient.sex, patient.birthday, patient.medsenger_contract, patient.email, patient.days)
            this.eventbus.emit('patient-updated', patient)
        }

        this.openPatientPage(patient)

    }
}

export default ProjectManager