import Model from "@/models/Model";
import {formatDateTime} from "@/utils/helpers";
import {v4 as uuidv4} from 'uuid';

class Submission extends Model {
    constructor(description, form) {
        super()
        this.init(description, form)
    }

    init(description, form) {
        super.init(description);

        this.project_id = description.project_id
        this.patient_id = description.patient_id
        this.form_id = description.form_id
        this.answers = description.answers
        this.records = description.records
        this.author = description.author
        this.created_on = new Date(description.created_on)
        this.form = form

        if (!this.answers) {
            this.answers = {}
        }

        // add existing records
        if (this.records) {
            this.records.forEach((record) => {
                if (!this.answers[record.params.part_id]) {
                    this.answers[record.params.part_id] = {}
                }
                if (!this.answers[record.params.part_id][record.params.group_key]) {
                    this.answers[record.params.part_id][record.params.group_key] = {}
                }

                this.answers[record.params.part_id][record.params.group_key][record.params.question_id] = record.value
            })
        }

        // add empty parts
        this.form.parts.forEach(part => {
            if (!part.repeatable && !this.answers[part.id]) {
                this.extend(part)
            }
        })
    }

    async save() {
        let description = undefined

        if (this.id) {
            description = await this._api.submission.update(this.project_id, this.patient_id, this.form_id, this.id, this.answers)
        } else {
            description = await this._api.submission.submit(this.project_id, this.patient_id, this.form_id, this.answers)
        }

        this.init(description, this.form)
    }

    reset() {
        this.init(this._backup, this.form)
    }

    remove(part, group_key) {
        delete this.answers[part.id][group_key]
    }

    extend(part) {
        const group_id = uuidv4()

        if (!this.answers[part.id]) {
            this.answers[part.id] = {}
        }

        this.answers[part.id][group_id] = {}

        part.fields.forEach(field => {
            if (field.type === 'select' || field.type === 'radio') {
                this.answers[part.id][group_id][field.id] = Object.values(field.params.options)[0]
            }
        })
    }

    static create(project, patient, form) {
        let submission = new Submission({
            project_id: project.id,
            patient_id: patient.id,
            form_id: form.id,
            answers: {}
        }, form)

        form.parts.forEach(part => {
            if (!part.repeatable) {
                submission.extend(part)
            }
        })

        return submission
    }

    get readable_created_on() {
        return formatDateTime(this.created_on)
    }
}

export default Submission