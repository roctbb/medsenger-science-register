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
        this.steps = description.steps
        this.settings = description.settings
        this.categories = {}

        description.categories.forEach((category) => {
            this.categories[category.id] = category
            this.categories[category.id].forms = []
        })

        this.categories[0] = {
            name: "Общее",
            priority: 0,
            forms: []
        }

        this.forms.forEach((form) => {
            if (form.category_id) {
                this.categories[form.category_id].forms.push(form)
            } else {
                this.categories[0].forms.push(form)
            }
        })

        if (this.categories[0].forms.length === 0) {
            delete this.categories[0]
        }

        this.form_groups = Object.values(this.categories)
        this.form_groups.sort((a, b) => b.priority - a.priority)
    }

    get patients() {
        return new Promise(resolve => {
            if (this._patients) {
                resolve(this._patients)
            } else {
                this._api.project.getPatients(this.id).then(patients => {
                    this._patients = patients.map((patient_description) => new Patient(this, patient_description))
                    resolve(this._patients)
                })
            }
        })
    }

    get groups() {
        return new Promise(resolve => {
            (this.patients).then(patients => {
                const create_group = (title, patients) => {
                    return {"title": title, "patients": patients}
                }

                console.log(this)

                if (!this.steps || !this.steps.length) {
                    resolve([create_group(undefined, patients)])
                } else {
                    let groups = []

                    this.steps.forEach(step => {
                        console.log(patients)
                        groups.push(create_group(step.title, patients.filter(patient => patient.step === step.title)))
                    })
                    console.log(groups)
                    resolve(groups)
                }
            })
        })
    }

    async refresh() {
        this._patients = undefined
        this.init(await this._api.project.get(this.id))
    }

    has_groups() {
        return this.form_groups.length !== 1
    }
}

export default Project