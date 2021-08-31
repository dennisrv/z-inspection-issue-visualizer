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

no_auth.get('/auth')

function getAll() {
    return no_auth.get('/nodes')
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

export default {
    getAll,
    createNewIssue,
    updateIssue,
    deleteIssue,
};