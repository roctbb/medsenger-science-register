import {empty} from "./helpers"

class HttpClient {
    constructor(endpoint, emitter) {
        this.endpoint = endpoint
        this.emitter = emitter
    }

    async makeRequest(action, method, body, headers) {
        console.log("Sending request ", method, " to ", this.endpoint + action, " with params ", body)

        let requestOptions = {
            method: method,
            body: body
        }

        if (headers) {
            requestOptions.headers = headers
        }

        try {

            this.signal('start')

            let result = await fetch(this.endpoint + action, requestOptions)

            console.log("Request done, status:", result.status)

            try {
                this.signal('end')
                return await result.json()
            } catch (e) {
                this.signal('end')
                return await result.text()
            }
        } catch (e) {
            this.signal('end')
            console.log("Request failed!")
            throw e
        }
    }

    signal(event) {
        if (this.emitter) {
            console.log("signaling ", 'http_' + event, "on", this.emitter)
            this.emitter.emit('http_' + event)
        }
    }

    async post(action, get_params, post_params) {
        if (!empty(get_params)) {
            action = action + '?' + new URLSearchParams(get_params).toString()
        }

        let data = new FormData()
        Object.keys(post_params).forEach((key) => {
            data.append(key, post_params[key])
        })

        return await this.makeRequest(action, 'POST', data)
    }

    async postJson(action, get_params, data, method) {
        if (empty(method)) {
            method = 'POST'
        }

        if (!empty(get_params)) {
            action = action + '?' + new URLSearchParams(get_params).toString()
        }

        let body = JSON.stringify(data)

        return await this.makeRequest(action, method, body, {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },)
    }

    async get(action, get_params) {
        if (!empty(get_params)) {
            action = action + '?' + new URLSearchParams(get_params).toString()
        }

        return await this.makeRequest(action, 'GET')
    }

    async delete(action, delete_params) {
        if (!empty(delete_params)) {
            action = action + '?' + new URLSearchParams(delete_params).toString()
        }

        return await this.makeRequest(action, 'DELETE')
    }
}

export default HttpClient