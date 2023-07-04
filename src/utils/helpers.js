let empty = function (obj) {
    return !obj || Object.keys(obj).length === 0
}

const external_url = (path) => {
    return process.env.VUE_APP_MAINHOST + path
}

const formatDate = (isodate) => {
    let d = new Date(isodate)
    return d.getDate() + "." + ('0' + (d.getMonth() + 1)).slice(-2) + "." + d.getFullYear()
}

const api_url = (action) => external_url('/api/client') + action

export {empty, external_url, api_url, formatDate}