import api_utils from "../api_utils";

class ProjectActions extends api_utils.ActionGroup {
    async getAll() {

        let query = {
            api_token: this.token
        }

        let result;

        try {
            result = await this.client.get('/projects', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async getPatients(project_id) {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.get('/project/' + project_id + '/patients', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async addPatient(project_id, name, sex, birthday) {

        let query = {
            api_token: this.token,
        }

        let data = {
            name: name,
            sex: sex,
            birthday: birthday
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
            ['AlreadyExists', 'Пациент уже добавлен.']
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async editPatient(project_id, patient_id, name, sex, birthday) {

        let query = {
            api_token: this.token,
        }

        let data = {
            name: name,
            sex: sex,
            birthday: birthday
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
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }
}

export default ProjectActions