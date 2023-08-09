import LoginScreen from "@/components/LoginScreen.vue";
import ProjectsScreen from "@/components/ProjectsScreen.vue";
import {createRouter, createWebHashHistory} from 'vue-router'
import resources from "@/resources"
import ProjectScreen from "@/components/ProjectScreen.vue";
import PatientScreen from "@/components/PatientScreen.vue";
import PatientEditorScreen from "@/components/PatientEditorScreen.vue";
import FormScreen from "@/components/FormScreen.vue";
import CompareScreen from "@/components/CompareScreen.vue";

const routes = [
    {path: '/', name: 'index'},
    {path: '/login', name: 'login', component: LoginScreen},
    {path: '/projects', name: 'projects', component: ProjectsScreen},
    {path: '/projects/:id', name: 'project', component: ProjectScreen, props: true},
    {path: '/projects/:project_id/patients/:id', name: 'patient', component: PatientScreen, props: true},
    {
        path: '/projects/:project_id/patients/:id/edit',
        name: 'edit_patient',
        component: PatientEditorScreen,
        props: true
    },
    {
        path: '/projects/:project_id/patients/create',
        name: 'create_patient',
        component: PatientEditorScreen,
        props: true
    },
    {
        path: '/projects/:project_id/patients/:patient_id/submissions/:submission_id',
        name: 'submission',
        component: FormScreen,
        props: true
    },
    {
        path: '/projects/:project_id/patients/:patient_id/form/:form_id',
        name: 'form',
        component: FormScreen,
        props: true
    },
    {
        path: '/projects/:project_id/patients/:patient_id/form/:form_id/compare',
        name: 'form_compare',
        component: CompareScreen,
        props: true
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

console.log("state manager in router:", resources.state)

router.beforeEach(async (to) => {
    if (!resources.state.loaded) {
        await resources.state.load()
    }

    console.log("User is ", resources.state.user)

    if (!resources.state.user && to.name !== 'login') {
        console.log(resources.state)
        console.log("redirecting to login")
        return {name: 'login'}
    }

    if (resources.state.user && to.name === 'login') {
        return {name: 'projects'}
    }

    if (to.name === 'index') {
        return {name: 'projects'}
    }
})

export default router