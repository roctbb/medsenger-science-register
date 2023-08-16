import api from "@/api"
import {formatDateTime} from "@/utils/helpers";

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

    get readable_created_on() {
        return formatDateTime(this.created_on)
    }
}

Model.prototype._api = api

export default Model