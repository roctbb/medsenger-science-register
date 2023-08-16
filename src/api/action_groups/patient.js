import api_utils from "../api_utils";

class PatientActions extends api_utils.ActionGroup {
    async add(project_id, name, sex, birthday, medsenger_contract, email, days, phone) {

        let query = {
            api_token: this.token,
        }

        let data = {
            name: name,
            sex: sex,
            birthday: birthday,
            email: email,
            days: days,
            phone: phone,
            medsenger_contract: medsenger_contract
        }

        let result;

        try {
            result = await this.client.postJson('/project/' + project_id + '/patients', query, data);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', 'Заполните все поля.'],
            ['AlreadyExists', 'Пациент уже добавлен.'],
            ['MedsengerAlreadyExists', 'Контракт с этим пациентом в Medsenger уже существует.'],
            ['IncorrectEmail', 'Проверьте правильность почтового адреса.'],
            ['IncorrectDays', 'Проверьте длительность контракта.'],
            ['IncorrectBirthday', 'Проверьте правильность даты рождения.'],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async edit(project_id, patient_id, name, sex, birthday, medsenger_contract, email, days, phone) {

        let query = {
            api_token: this.token,
        }

        let data = {
            name: name,
            sex: sex,
            birthday: birthday,
            phone: phone,
            email: email,
            days: days,
            medsenger_contract: medsenger_contract
        }

        let result;

        try {
            result = await this.client.postJson('/project/' + project_id + '/patients/' + patient_id, query, data, 'PUT');
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', 'Заполните все поля.'],
            ['MedsengerAlreadyExists', 'Контракт с этим пациентом в Medsenger уже существует.'],
            ['IncorrectEmail', 'Проверьте правильность почтового адреса.'],
            ['IncorrectDays', 'Проверьте длительность контракта.'],
            ['IncorrectBirthday', 'Проверьте правильность даты рождения.'],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async addComment(project_id, patient_id, text, description) {

        let query = {
            api_token: this.token,
        }

        let data = {
            text: text,
            description: description
        }

        let result;

        try {
            result = await this.client.postJson('/project/' + project_id + '/patients/' + patient_id + '/comments', query, data, 'POST');
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', 'Заполните все поля.'],
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }
}

export default PatientActions