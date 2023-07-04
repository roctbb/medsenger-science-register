class User {
    constructor(description) {
        this.email = description.email
        this.name = description.name
        this.api_token = description.api_token
        this.clinic = description.clinic
    }

}

export default User