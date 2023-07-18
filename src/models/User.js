import Model from "@/models/Model";
import Project from "@/models/Project";

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
        this.projects = description.projects.map(project => new Project(project))
    }
}

export default User