let empty = function (obj) {
    return !obj || Object.keys(obj).length === 0
}

const external_url = (path) => {
    return process.env.VUE_APP_MAINHOST + path
}

const formatDate = (isodate) => {
    let d = new Date(isodate)
    console.log(d)
    return d.getDate() + "." + ('0' + (d.getMonth() + 1)).slice(-2) + "." + d.getFullYear()
}

const formatDateTime = (isodate) => {
    let d = new Date(isodate)
    return d.getDate() + "." + ('0' + (d.getMonth() + 1)).slice(-2) + "." + d.getFullYear() + " " + d.getHours() + ":" + ('0' + d.getMinutes()).slice(-2)
}

const copy = function (obj) {
    return JSON.parse(JSON.stringify(obj))
}


const api_url = (action) => external_url('/api/client') + action

export {empty, external_url, api_url, formatDate, formatDateTime, copy}