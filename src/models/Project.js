import Model from "@/models/Model";
import Patient from "@/models/Patient";

class Project extends Model {
    constructor(description) {
        super()
        this.init(description)
    }

    init(description) {
        super.init(description);

        this._patients = undefined
        this.name = description.name
        this.forms = description.forms
    }

    get patients() {
        return new Promise(resolve => {
            if (this._patients) {
                resolve(this._patients)
            } else {
                this._api.project.getPatients(this.id).then(patients => {
                    this._patients = patients.map((patient_description) => new Patient(this.id, patient_description))
                    resolve(this._patients)
                })
            }
        })
    }
}

export default Project