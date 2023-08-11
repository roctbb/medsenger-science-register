import api from "@/api"

class Model {
    init(description) {
        this._backup = description

        if (description) {
            this.id = parseInt(description.id)
        }
    }

    save() {

    }

    reset() {
        this.init(this._backup)
    }
}

Model.prototype._api = api

export default Model