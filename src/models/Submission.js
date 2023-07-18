import Model from "@/models/Model";
import {formatDateTime} from "@/utils/helpers";

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
        this.created_on = description.created_on

        if (!this.answers) {
            this.answers = {}
        }

        if (this.records) {
            this.records.forEach((record) => {
                this.answers[record.params.question_id] = record.value
            })
        }
    }

    async save() {
        let description = await this._api.submission.submit(this.project_id, this.patient_id, this.form_id, this.answers)
        this.init(description)
    }

    static create(project_id, patient_id, form_id) {
        return new Submission({
            project_id: project_id,
            patient_id: patient_id,
            form_id: form_id,
            answers: {}
        })
    }

    get readable_created_on() {
        return formatDateTime(this.created_on)
    }
}

export default Submission