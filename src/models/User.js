import Model from "@/models/Model";
import Project from "@/models/Project";
import {empty} from "@/utils/helpers";

class User extends Model {
    constructor(description) {
        super();

        this.init(description)
    }

    init(description) {
        super.init(description)

        this.email = description.email
        this.name = description.name
        this.api_token = description.api_token
        this.clinic = description.clinic
        this.specialties = description.specialties
        this.projects = description.projects.map(project => new Project(project))
    }

    is(specialty) {
        if (empty(this.specialties)) {
            return false
        }
        if (this.specialties.includes('администратор'))
        {
            return true;
        }
        return this.specialties.includes(specialty)
    }
}

export default User