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
            ['InsufficientData', "Аккаунт с таким логином не найден. Проверьте правильность почты / телефона."],
            ['User is not activated', "Ваш аккаунт еще не активирован. Чтобы активировать аккаунт, найдите в почте письмо от Medsenger и перейдите по ссылке в нем."],
            ['User is deleted', "Аккаунт удален. Обратитесь в техническую поддержку."],
            ['Incorrect password', "Неправильный пароль."],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    // returns User with token
    async check() {

        let query = {
            api_token: this.token
        }

        let result;

        try {
            result = await this.client.get('/check', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['Incorrect data', "Необходимо снова войти в систему."],
            ['User is deleted', "Аккаунт удален. Обратитесь в техническую поддержку."],
            ['Incorrect hash', "Необходимо снова войти в систему."],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }
}

export default AccountActions