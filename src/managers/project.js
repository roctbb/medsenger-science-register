import Manager from "@/managers/common";

class ProjectManager extends Manager {
    async getPatients(project) {
        return await this.api.project.getPatients(project.id)
    }

    open(project) {
        this.eventbus.emit('change-screen', 'project-patients')
        this.eventbus.emit('project-selected', project)
    }
}

export default ProjectManager