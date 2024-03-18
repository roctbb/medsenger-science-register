<template>
    <div v-if="groups">
        <div>
            <table class="table table-striped">
                <thead>
                <tr>
                    <th scope="col" v-for="(column_title, i) in column_titles" :key="i"><a
                        @click="sort_index = i">{{ column_title }}</a></th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(row, i) in sortPatients(filterPatients(rows))" :key="i">
                    <td v-for="(value, j) in row" :key="j">{{ value }}</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>


import {empty, formatDate, isString} from "@/utils/helpers";

export default {
    name: 'PatientsTable',
    props: ['groups', 'project', 'search_field'],
    data() {
        return {
            column_titles: ['ID', 'ФИО', 'Врач', 'Дата рождения'],
            columns: ['id', 'name', 'created_by', 'readable_birthday'],
            rows: [],
            sort_index: 0
        }
    },
    methods: {
        formatDate,
        sortPatients: function (rows) {
            const comp = (a, b) => {
                if (!a[this.sort_index]) return 1;
                if (!b[this.sort_index]) return -1;
                if (isString(a[this.sort_index])) {
                    return a[this.sort_index].toLowerCase().localeCompare(b[this.sort_index].toLowerCase())
                } else {
                    return a[this.sort_index] - b[this.sort_index]
                }
            }

            rows.sort(comp)
            return rows
        },
        filterPatients: function (rows) {
            return rows.filter((row) => empty(this.search_field) || row.filter(value => value && value.toString().toLowerCase().includes(this.search_field.toLowerCase())).length > 0)
        }
    },
    async mounted() {
        let patients = []

        if (this.groups.length > 1) {
            this.column_titles.push('Этап')
            this.columns.push('group_title')

            this.groups.forEach((group, i) => {
                let group_patients = group.patients
                group_patients.forEach(patient => {
                    patient.group_title = "Шаг " + (i + 1) + ". " + group.title
                })
                patients.push(...group_patients)
            })

        } else {
            patients = this.groups[0].patients
        }
        let show_off_fields = new Set()

        patients.forEach(patient => {
            patient.show_off_records.forEach(field => {
                show_off_fields.add("show_off_" + field.title)
                patient["show_off_" + field.title] = field.value
            })
        })

        show_off_fields.forEach(title => {
            this.column_titles.push(title.replace("show_off_", ""))
            this.columns.push(title)
        })

        patients.forEach(patient => {
            let row = []

            this.columns.forEach(column => {
                row.push(patient[column])
            })

            this.rows.push(row)
        })

    }
}
</script>

<style scoped>

</style>
