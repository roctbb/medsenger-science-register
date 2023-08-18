import Model from "@/models/Model";
import {formatDate} from "@/utils/helpers";
import Submission from "@/models/Submission";
import Comment from "@/models/Comment";
import PatientFile from "@/models/PatientFile";

class Patient extends Model {
    constructor(project, description) {
        super(description)
        this._submissions = undefined
        this._files = undefined
        this.init(project, description)
    }

    init(project, description) {
        super.init(description);

        if (description) {
            this.name = description.name
            this.sex = description.sex
            this.birthday = description.birthday
            this.contract_id = description.contract_id
            this.email = description.email
            this.days = description.days
            this.created_by = description.created_by
            this.phone = description.phone
            this.comments = []
            this.step = description.step

            if (description.comments) {
                description.comments.forEach(comment => {
                    this.comments.push(new Comment(comment))
                })
            }

            if (this.contract_id) {
                this.medsenger_contract = true
            } else {
                this.medsenger_contract = false
            }
        } else {
            this.sex = 'male'
        }

        this.project = project
        this.project_id = project.id
    }

    get readable_birthday() {
        return formatDate(new Date(this.birthday))
    }

    async add_comment(text) {
        let comment = await this._api.patient.addComment(this.project_id, this.id, text)
        this.comments.push(new Comment(comment))
    }


    async save() {
        if (this.id) {
            let description = await this._api.patient.edit(this.project_id, this.id, this.name, this.sex, this.birthday, this.medsenger_contract, this.email, this.days, this.phone)
            this.init(this.project, description)
        } else {
            let description = await this._api.patient.add(this.project_id, this.name, this.sex, this.birthday, this.medsenger_contract, this.email, this.days, this.phone)
            this.init(this.project, description)
        }
    }

    async refresh() {
        if (this.id) {
            let description = await this._api.patient.get(this.project_id, this.id)
            this.init(this.project, description)
        }
    }

    reset() {
        this.init(this.project, this._backup)
    }

    get submissions() {
        return new Promise(resolve => {
            if (this._submissions) {
                resolve(this._submissions)
            } else {
                this._api.submission.all(this.project_id, this.id).then(submissions => {
                    this._submissions = submissions.map((submission) => new Submission(submission, this.project.forms.find(f => f.id === submission.form_id)))
                    resolve(this._submissions)
                })
            }
        })
    }

    get files() {
        return new Promise(resolve => {
            if (this._files) {
                resolve(this._files)
            } else {
                this._api.file.getAll(this.project_id, this.id).then(files => {
                    this._files = files.map((file) => new PatientFile(file))
                    resolve(this._files)
                })
            }
        })
    }
}

export default Patient