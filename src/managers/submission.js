import Manager from "@/managers/common";

class SubmissionManager extends Manager {
    openFillPage(form) {
        this.eventbus.emit('change-screen', 'fill-form')
        this.eventbus.emit('form-selected', form)
    }

    openSubmissionPage(form) {
        this.eventbus.emit('change-screen', 'fill-form')
        this.eventbus.emit('form-selected', form)
        this.eventbus.emit('submission-selected', form)
    }

    async getAll(project, patient) {
        return await this.api.submission.getAll(project.id, patient.id)
    }

    async add(project, patient, form, answers) {
        let submission = await this.api.submission.submit(project.id, patient.id, form.id, answers)

        this.eventbus.emit('change-screen', 'patient')
        this.eventbus.emit('submission-added', submission)
    }
}

export default SubmissionManager