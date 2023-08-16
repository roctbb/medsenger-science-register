import Model from "@/models/Model";

class Comment extends Model {
    constructor(description) {
        super()
        this.init(description)
    }

    init(description) {
        super.init(description);

        this.text = description.text
        this.description = description.description
        this.author = description.author
        this.created_on = description.created_on
    }
}

export default Comment