import Manager from "@/managers/common";

class UserManager extends Manager {

    async update(updatedUser) {
        this.state.user = await this.api.account.changeProfile({
            email: updatedUser.email,
            name: updatedUser.name
        })
    }

    async updatePassword(password) {
        this.state.user = await this.api.account.changePassword({
            password: password
        })
    }
}

export default UserManager