import Model from "@/models/Model";
import {formatDateTime} from "@/utils/helpers";
import downloadjs from "downloadjs";

class PatientFile extends Model {
    constructor(description) {
        super()
        this.init(description)
    }

    init(description) {
        super.init(description);

        this.project_id = description.project_id
        this.patient_id = description.patient_id
        this.doctor_id = description.doctor_id

        this.name = description.name
        this.type = description.type
        this.path = description.path
        this.file_name = description.file_name

        this.base64 = description.base64
        this.size = description.size

        this.created_on = new Date(description.created_on)
    }

    async save() {
        let description = undefined

        if (this.id) {
            description = await this._api.file.update(this.project_id, this.patient_id, this.id, this.name)
        } else {
            let file_dict = {
                base64: this.base64,
                type: this.type,
                file_name: this.file_name,
                name: this.name
            }
            console.log(file_dict)
            description = await this._api.file.upload(this.project_id, this.patient_id, file_dict)
        }

        this.init(description)
    }

    download() {
        this._api.file.download(this.project_id, this.patient_id, this.id).then((full_file) => {
            console.log(full_file)
            downloadjs(`data:${full_file.type};base64,${full_file.base64}`, full_file.file_name, full_file.type);
        })
    }

    async delete() {
        await this._api.file.delete(this.project_id, this.patient_id, this.id)
    }

    reset() {
        this.init(this._backup)
    }


    static create(project, patient, file) {
        let new_file = new PatientFile({
            project_id: project.id,
            patient_id: patient.id,
            base64: file.base64,
            type: file.type,
            file_name: file.file_name,
            name: file.name
        })

        return new_file
    }

    get readable_created_on() {
        return formatDateTime(this.created_on)
    }

}

export default PatientFile