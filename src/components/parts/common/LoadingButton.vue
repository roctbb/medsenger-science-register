<script setup>

</script>

<template>
    <button class="btn btn-primary" :class="class_name" :disabled="disabled">
        <slot v-if="!disabled"></slot>
        <span v-else>Загрузка...</span>
    </button>
</template>

<script>
export default {
    name: 'LoadingButton',
    props: ['class_name'],
    data() {
        return {
            disabled: false
        }
    },
    methods: {
        enable: function () {
            this.disabled = false
        },
        disable: function () {
            this.disabled = true
        }

    },
    async mounted() {
        this.event_bus.on('http_start', this.disable)
        this.event_bus.on('http_end', this.enable)
    }
}
</script>