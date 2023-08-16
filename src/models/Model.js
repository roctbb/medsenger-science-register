import api from "@/api"
import {formatDateTime} from "@/utils/helpers";

class Model {
    init(description) {
        this._backup = description

        if (description) {
            this.id = parseInt(description.id)

            if (description.created_on) {
                this.created_on = new Date(description.created_on)
            }

        }
    }

    save() {

    }

    reset() {
        this.init(this._backup)
    }

    get readable_created_on() {
        return formatDateTime(this.created_on)
    }
}

Model.prototype._api = api

export default Model