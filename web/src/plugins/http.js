import axios from 'axios'

const API_URL = '/api'

const no_auth = axios.create({
    baseURL: API_URL,
    headers: {
        post: {
            "Content-Type": "application/json"
        }
    }
});

const with_auth = axios.create({
    baseURL: API_URL,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    withCredentials: true,
    headers: {
        post: {
            "Content-Type": "application/json"
        }
    },
})

no_auth.get('/auth').then(() => console.log("Cookie set"))

function getAll() {
    return no_auth.get('/nodes')
}

function getFiltered(searchText, related) {
    return no_auth.get('/nodes', {
        params:
            {
                searchText: searchText,
                related: related
            }
    })
}

function createNewIssue(postData) {
    return with_auth.post('/nodes/', postData)
}

function updateIssue(issueId, postData) {
    return with_auth.post(`/nodes/${issueId}`, postData)
}

function deleteIssue(issueId) {
    return with_auth.delete(`/nodes/${issueId}`)
}

function mergeIssues(mergeData) {
    return with_auth.post('/nodes/merge', mergeData)
}

function uploadFile(fileToUpload) {
    let formData = new FormData()
    formData.append('issues', fileToUpload)

    return with_auth.post('/nodes/import', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export default {
    getAll,
    getFiltered,
    createNewIssue,
    updateIssue,
    deleteIssue,
    mergeIssues,
    uploadFile,
};