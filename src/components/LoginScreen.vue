<template>
    <div class="row">
        <div class="col-xl-5" id="left_block">
            <div class="row align-items-center" style="height: 100vh;">
                <div class="col-12 p-md-5 mb-5">
                    <div class="card">
                        <div class="card-body m-2">
                            <img class="my-3" src="/images/logo_tele.svg" style="width: 70%; max-width: 400px;"/>

                            <h4 class="my-3">Вход в регистр онкофертильности</h4>

                            <div class="alert alert-warning" v-if="error">
                                {{ error }}
                            </div>

                            <form>
                                <div class="mb-3">
                                    <label class="form-label">Email</label>
                                    <input type="email" class="form-control" aria-describedby="emailHelp"
                                           v-model="email">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Пароль</label>
                                    <input type="password" class="form-control" v-model="password">
                                </div>

                                <button type="submit" @click="makeLogin" class="btn btn-primary">Войти</button>

                                <div class="mt-3">
                                    <a target="_blank" class="colored-link"
                                       href="https://telegynecology.ru/info/pat/47#libs">Материалы
                                        для пациентов</a>
                                </div>
                            </form>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>


export default {
    name: 'LoginScreen',
    components: {},
    data() {
        return {
            email: "",
            password: "",
            error: ""
        }
    },
    methods: {
        makeLogin: async function (e) {
            e.preventDefault();
            try {
                this.error = undefined
                await this.managers.auth.makeLogin(this.email, this.password)
                console.log("pushing projects route")
                this.$router.push({name: 'projects'})
            } catch (e) {
                this.error = e.message
            }
        }
    },
}
</script>

<style scoped>
#left_block {
    background-color: #029DAF;
}
</style>
