<template>
    <h3 class="my-3">Вход в регистр</h3>

    <div class="alert alert-warning" v-if="error">
        {{ error }}
    </div>

    <form>
        <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" aria-describedby="emailHelp" v-model="email">
        </div>
        <div class="mb-3">
            <label class="form-label">Пароль</label>
            <input type="password" class="form-control" v-model="password">
        </div>

        <div class="mb-3" v-if="can_reset_password">
            <a href="/password/link">Восстановление пароля</a>
        </div>

        <button type="submit" @click="makeLogin" class="btn btn-primary">Войти</button>
    </form>
</template>

<script>


export default {
    name: 'LoginScreen',
    components: {},
    data() {
        return {
            email: "",
            password: "",
            error: "",
            can_reset_password: !process.env.VUE_APP_MEDSENGER_LOGIN
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

</style>
