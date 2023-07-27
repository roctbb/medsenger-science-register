import Model from "@/models/Model";
import {formatDateTime} from "@/utils/helpers";
import {v4 as uuidv4} from 'uuid';

class Submission extends Model {
    constructor(description) {
        super()
        this.init(description)
    }

    init(description) {
        super.init(description);

        this.project_id = description.project_id
        this.patient_id = description.patient_id
        this.form_id = description.form_id
        this.answers = description.answers
        this.records = description.records
        this.author = description.author
        this.created_on = description.created_on

        if (!this.answers) {
            this.answers = {}
        }

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
    }

    async save() {
        let description = await this._api.submission.submit(this.project_id, this.patient_id, this.form_id, this.answers)
        this.init(description)
    }

    remove(part, group_key) {
        delete this.answers[part.id][group_key]
    }

    extend(part) {
        this.answers[part.id][uuidv4()] = {}
    }

    static create(project_id, patient_id, form) {
        let submission = new Submission({
            project_id: project_id,
            patient_id: patient_id,
            form_id: form.id,
            answers: {}
        })

        form.parts.forEach(part => {
            submission.answers[part.id] = {}

            if (!part.repeatable) {
                submission.answers[part.id][uuidv4()] = {}
            }
        })

        return submission
    }

    get readable_created_on() {
        return formatDateTime(this.created_on)
    }
}

export default Submission