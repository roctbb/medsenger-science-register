import Model from "@/models/Model";
import {v4 as uuidv4} from 'uuid';
import {formatDate} from "@/utils/helpers";
import {reactive} from "vue";

class Submission extends Model {
    constructor(description, form) {
        super()
        this.init(description, form)
    }

    init(description, form) {
        super.init(description);

        console.log(description)

        this.project_id = description.project_id
        this.patient_id = description.patient_id
        this.form_id = description.form_id
        this.answers = description.answers
        this.records = description.records
        this.author = description.author
        this.form = form

        console.log("Initializing submission")

        if (!this.answers || this.answers === {}) {
            console.log("creating reactive answers")
            this.answers = reactive({})
        }
        else {
            console.log("answers is ", this.answers)
        }

        // add existing records
        if (this.records) {
            this._fillRecords(this.records)
        }

        // add empty parts
        this.form.parts.forEach(part => {
            if (!part.repeatable && !this.answers[part.id]) {
                this.extend(part)
            }
        })

        if (!this.id) {
            console.log("before", this.answers)
            this._api.submission.get_saved_answers(this.project_id, this.patient_id, this.form_id).then(records => {
                console.log(this.answers)
                records.forEach((record) => {
                    this.answers[record.params.part_id][Object.keys(this.answers[record.params.part_id])[0]][record.params.question_id] = record.value
                })
            })
        }
    }

    _fillRecords(records) {
        records.forEach((record) => {
            if (!this.answers[record.params.part_id]) {
                this.answers[record.params.part_id] = {}
            }
            if (!this.answers[record.params.part_id][record.params.group_key]) {
                this.answers[record.params.part_id][record.params.group_key] = {}
            }

            this.answers[record.params.part_id][record.params.group_key][record.params.question_id] = record.value
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

    async delete() {
        if (this.id) {
            await this._api.submission.delete(this.project_id, this.patient_id, this.id)
        }
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

        if (!this.id) {
            part.fields.forEach(field => {
                if (field.type === 'select' || field.type === 'radio') {
                    this.answers[part.id][group_id][field.id] = Object.values(field.params.options)[0]
                }
            })
        }

    }

    _iterate_fields(F) {
        this.form.parts.forEach(part => {
            if (this.answers[part.id]) {
                Object.keys(this.answers[part.id]).forEach((group_id) => {
                    part.fields.forEach(field => {
                        F(part, group_id, field)
                    })
                })
            }
        })
    }

    show_off_fields() {
        let fields = []

        this._iterate_fields((part, group_id, field) => {
            if (field.params && field.params.show_off && this.answers[part.id][group_id][field.id]) {
                let description = {
                    "title": field.params.show_off_title,
                    "value": this.answers[part.id][group_id][field.id]
                }

                if (field.params.show_off_transform === "date") {
                    description["value"] = formatDate(new Date(description["value"]))
                }

                fields.push(description)
            }
        })

        return fields
    }

    import(answers) {
        this._iterate_fields((part, group_id, field) => {
            if (answers[field.text]) {
                this.answers[part.id][group_id][field.id] = answers[field.text]
            }

            if (field.params && field.params.external_title && answers[field.params.external_title]) {
                this.answers[part.id][group_id][field.id] = answers[field.params.external_title]
            }
        })
    }

    static create(project, patient, form) {
        return new Submission({
            project_id: project.id,
            patient_id: patient.id,
            form_id: form.id,
        }, form)
    }
}

export default Submission