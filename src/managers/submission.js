import Manager from "@/managers/common";

class SubmissionManager extends Manager {

    async all(project, patient) {
        return await this.api.submission.all(project.id, patient.id)
    }

    async add(project, patient, form, answers) {
        let submission = await this.api.submission.submit(project.id, patient.id, form.id, answers)

        this.eventbus.emit('change-screen', 'patient')
        this.eventbus.emit('submission-added', submission)
    }
}

export default SubmissionManager