import api_utils from "../api_utils";

class FileActions extends api_utils.ActionGroup {
    async getAll(project_id, patient_id) {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.get('/project/' + project_id + '/patients/' + patient_id + '/files', query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = []

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async upload(project_id, patient_id, file) {

        let query = {
            api_token: this.token,
        }

        let data = {
            file: file
        }

        let result;

        try {
            result = await this.client.postJson('/project/' + project_id + '/patients/' + patient_id + '/files', query, data);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['InsufficientData', 'Заполните все обязательные поля']
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async download(project_id, patient_id, file_id) {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.get('/project/' + project_id + '/patients/' + patient_id + '/files/' + file_id, query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['NotFound', 'Файл не найден'],
            ['AccessDenied',  'Нет доступа к файлу']
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result.data

    }

    async delete(project_id, patient_id, file_id) {

        let query = {
            api_token: this.token,
        }

        let result;

        try {
            result = await this.client.delete('/project/' + project_id + '/patients/' + patient_id + '/files/' + file_id, query);
        } catch (e) {
            console.log(e)
            throw new Error("Ошибка соединения с сервером.")
        }

        let expectedErrors = [
            ['NotFound', 'Файл не найден'],
            ['AccessDenied',  'Нет доступа к файлу']
        ]

        api_utils.checkForErrors(result, expectedErrors)

        return result

    }

}

export default FileActions