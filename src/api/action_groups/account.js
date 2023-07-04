import api_utils from "../api_utils";

class AccountActions extends api_utils.ActionGroup {
    // returns User with token
    async login(login, password) {

        let query = {
            email: login,
            password: password,
        }

        let result;

        try {
            result = await this.client.get('/auth', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', "Введите логин и пароль."],
            ['NotFound', "Пользователь с такой почтой не найден."],
            ['IncorrectPassword', "Неправильный пароль."],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    // returns User with token
    async get_user() {

        let query = {
            api_token: this.token
        }

        let result;

        try {
            result = await this.client.get('/user', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['IncorrectToken', "Необходимо снова войти в систему."],
            ['ExpiredToken', "Необходимо снова войти в систему."],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }
}

export default AccountActions