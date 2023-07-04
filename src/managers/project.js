import Manager from "@/managers/common";

class ProjectManager extends Manager {
    async getPatients(project) {
        return await this.api.project.getPatients(project.id)
    }

    open(project) {
        this.eventbus.emit('change-screen', 'project-patients')
        this.eventbus.emit('project-selected', project)
    }

    openPatientPage(project, patient) {
        this.eventbus.emit('change-screen', 'patient')
        this.eventbus.emit('patient-selected', patient)
    }

    addPatientPage() {
        this.eventbus.emit('change-screen', 'add-patient')
    }

    async addPatient(project, newPatient) {
        let patient = await this.api.project.addPatient(project.id, newPatient.name, newPatient.sex, newPatient.birthday)
        this.openPatientPage(project, patient)
    }
}

export default ProjectManager