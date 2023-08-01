import Model from "@/models/Model";
import {formatDate} from "@/utils/helpers";
import Submission from "@/models/Submission";

class Patient extends Model {
    constructor(project_id, description) {
        super(description)
        this._submissions = undefined
        this.init(project_id, description)
    }

    init(project_id, description) {
        super.init(description);

        if (description) {
            this.name = description.name
            this.sex = description.sex
            this.birthday = description.birthday
            this.contract_id = description.contract_id
            this.email = description.email
            this.days = description.days

            if (this.contract_id) {
                this.medsenger_contract = true
            } else {
                this.medsenger_contract = false
            }
        }
        else {
            this.sex = 'male'
        }

        this.project_id = project_id
    }

    get readable_birthday() {
        return formatDate(this.birthday)
    }


    async save() {
        if (this.id) {
            let description = await this._api.project.editPatient(this.project_id, this.id, this.name, this.sex, this.birthday, this.medsenger_contract, this.email, this.days)
            this.init(this.project_id, description)
        } else {
            let description = await this._api.project.addPatient(this.project_id, this.name, this.sex, this.birthday, this.medsenger_contract, this.email, this.days)
            this.init(this.project_id, description)
        }
    }

    reset() {
        this.init(this.project_id, this._backup)
    }

    get submissions() {
        return new Promise(resolve => {
            if (this._submissions) {
                resolve(this._submissions)
            } else {
                this._api.submission.getAll(this.project_id, this.id).then(submissions => {
                    this._submissions = submissions.map((submission) => new Submission(submission))
                    resolve(this._submissions)
                })
            }
        })
    }
}

export default Patient