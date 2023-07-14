<template>
    <div id="main" class="container">
    <h6 style="text-align: center; color: darkgrey;">{{ is_edit? "Редактируем" : "Создаём" }} анкету с названием</h6>
    <p style="text-align: center; font-size: 15pt;">{{name!=""? name : "(Без названия)"}}</p>

    <div class="card my-3">
        <div class="card-body">
            <div class="row">
                <label class="col-md-4 col-form-label text text">
                    Название
                </label>
                <div class="col-md-8">
                    <input type="text" id="name" class="form-control" v-model="name" onfocus="this.select()">
                </div>
            </div>
        </div>
    </div>


    <div v-for="(question, i) in questions" class="mt-3" :key="i">
        <div class="card">
            <div class="card-body">
                <h5 class="bold-text">
                    Вопрос №{{ i + 1 }}
                    &nbsp;
                    <button class="change_number_button" @click="go_down(i)" v-if="i!=questions.length-1">
                        ⬇
                    </button>
                    <button class="change_number_button" @click="go_up(i)" v-if="i!=0">
                        ⬆
                    </button>
                    &nbsp;
                    <span style="font-size: 9pt; color: darkgrey; font-weight: normal;"
                          v-if="i!=0 || i!=questions.length-1">
                            Вы можете управлять расположением вопросов нажимая на стрелки
                        </span>
                </h5>

                <div class="row my-2">
                    <label class="col-md-4 col-form-label text text">
                        Текст
                    </label>
                    <div class="col-md-8">
                        <input type="text" v-model="question.text" class="form-control">
                    </div>
                </div>

                <div class="row my-2">
                    <label class="col-md-4 col-form-label text">
                        Категория
                    </label>
                    <div class="col-md-8">
                        <input type="text" v-model="question.category" class="form-control">
                    </div>
                </div>

                <div class="row my-2">
                    <label class="col-md-4 col-form-label text">
                        Обязательный вопрос?
                    </label>
                    <div class="col-md-8 col-form-label">
                        <div class="form-check form-switch">
                            <input type="checkbox" class="form-check-input" :id="'required_question_setter_' + i"
                                   v-model="question.required">
                            <label :for="'required_question_setter_' + i">
                                Сейчас это <span style="color: rgba(255, 0, 0, 0.637);">{{ question.required==true? "обязательный" : "необзательный" }}</span>
                                вопрос
                            </label>
                        </div>
                    </div>
                </div>

                <div class="row my-2">
                    <div class="col-md-4 col-form-label text">
                        Тип
                    </div>
                    <div class="col-md-8 col-form-label">
                        <select class="form-select" v-model="question.type">
                            <option value="string">Строка</option>
                            <option value="integer">Целое число</option>
                            <option value="float">Дробное число</option>
                            <option value="text">Текст</option>
                            <option value="date">Дата</option>
                            <option value="checkbox">Галочка</option>
                            <option value="enum">Выбор варианта</option>
                        </select>
                    </div>
                </div>

                <div class="row my-2">
                    <div class="col-md-4 col-form-label text">
                        Описание
                    </div>
                    <div class="col-md-8 col-form-label">
                        <textarea class="form-control" rows="3" v-model="question.description"></textarea>
                    </div>
                </div>

                <template v-if="question.type=='checkbox'">
                    <!-- <hr> -->
                    <div class="row my-2">
                        <label class="col-md-4 col-form-label">
                            Значение, если галочка поставлена
                        </label>
                        <label class="col-md-8 col-form-label">
                            <input type="text" class="form-control" v-model="questions[i].checker.true">
                        </label>
                    </div>
                    <div class="row my-2">
                        <label class="col-md-4 col-form-label">
                            Значение, если галочка не поставлена
                        </label>
                        <label class="col-md-8 col-form-label">
                            <input type="text" class="form-control" v-model="questions[i].checker.false">
                        </label>
                    </div>
                </template>

                <template v-if="question.type=='enum'">
                    <!-- <hr> -->
                    <div class="row">
                        <h6 class="bold-text">Варианты:</h6>
                        <div class="col-md-6 col-form-label" style="text-align: center;"
                             v-if="questions[i].variants.length > 0">
                            Отображаемый текст
                        </div>
                        <div class="col-md-5 col-form-label" style="text-align: center;"
                             v-if="questions[i].variants.length > 0">
                            Значение
                        </div>
                        <div class="col-md-1 col-form-label" v-if="questions[i].variants.length > 0">

                        </div>
                        <div v-else>
                            <h5 style="text-align: center;">
                                Вариантов нет...
                            </h5>
                        </div>
                    </div>

                    <template v-for="(variant, j) in question.variants" :key="j">
                        <div class="row">
                            <label class="col-md-6 col-form-label">
                                <input type="text" class="form-control form-control-sm" v-model="variant.text">
                            </label>
                            <label class="col-md-5 col-form-label">
                                <input type="text" class="form-control form-control-sm" v-model="variant.value">
                            </label>
                            <label class="col-md-1 col-form-label">
                                <input type="button" class="btn btn-sm btn-danger" value="Удалить"
                                       @click="deleteParam(i, j)">
                            </label>
                        </div>
                    </template>
                    <div style="font-size: 9pt; color: darkgrey; font-weight: normal;">
                        При сохранении анкеты, пары "текст" - "значение", в которых отсутствует значение, будут
                        проигнорированы
                    </div>
                    <button class="btn btn-primary btn-sm my-2" @click="add_new_param_line(question)">Добавить вариант
                    </button>
                </template>

                <div class="row my-2">
                    <div></div>
                </div>

                <hr>

                <button type="button" class="btn btn-sm btn-danger" @click="deleteQuestion(i)">Удалить вопрос №{{ i+1
                    }}
                </button>

                <div style="color: darkgrey; font-size: 9pt; margin-top: 5px;">
                    При удалении вопроса все остальные вопросы будут смещены на один номер назад без потери
                    введённых данных.
                    <br>
                    Удалённый вопрос невозможно восстановить.
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-4 col-form-label text">
            <button class="btn btn-primary" @click="add_question()">Добавить вопрос</button>
        </div>
    </div>

    <div class="d-grid my-4">
        <div></div>
    </div>
    <div class="d-grid my-4">
        <div></div>
    </div>

    <div class="d-grid my-4">
        <button class="btn btn-primary btn-lg" @click="save()" type="submit">Сохранить анкету</button>
    </div>

    <div class="d-grid my-4">
        <div></div>
    </div>
    </div>
</template>

<script>
window.FORM = JSON.parse('{{ form_json | safe }}')
console.log(window.FORM)

function create_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

export default {
  name: 'EditorAllScreen',
  components: {},
  data() {
    return{
        isLoaded: false,
        questions: [],
        name: "Новая анкета",
        json: {},
        is_edit: false
    }
  },
  created() {
        if (window.FORM)
        {
            this.questions = window.FORM.fields;
            this.name = window.FORM.name;
        }

        if(this.questions.length > 0){
            let j;
            this.is_edit = true

            for(let i = 0; i<this.questions.length; i++){
                this.questions[i].variants = [{"text": "","value": ""},{"text": "","value": ""}]
                this.questions[i].checker = {"true": "","false": ""}

                if(this.questions[i].type == 'enum'){
                    let iter = 0
                    for(j in this.questions[i].params.options){
                        if(iter >= this.questions[i].variants.length){
                            this.questions[i].variants.push({"text": "","value": ""})
                        }
                        this.questions[i].variants[iter].text = j
                        this.questions[i].variants[iter].value = this.questions[i].params.options[j]
                        iter++
                    }
                }
                else if(this.questions[i].type == 'checkbox'){
                    this.questions[i].checker.true = this.questions[i].params.options.true
                    this.questions[i].checker.false = this.questions[i].params.options.false
                }

                this.questions[i].params = {"options": {}}
            }
        }
        else{
            this.add_question()
        }
    },
    methods: {
        add_question() {
            this.questions.push({
                "text": "",
                "category": "",
                "params": {"options": {}},
                "required": false,
                "type": "string",
                "id": create_UUID(),
                "description": "",
                "variants": [
                    {
                        "text": "",
                        "value": ""
                    },
                    {
                        "text": "",
                        "value": ""
                    }
                ],
                "checker": {
                    "true": "",
                    "false": ""
                },
            })
        },

        add_new_param_line(question){
            question.variants.push({
                "text": "",
                "value": ""
            })
        },

        deleteParam(question_number, variant_number){
            this.questions[question_number].variants.splice(variant_number, 1)
        },

        save(){
            let question_number, variant_number, variant;
            let result_questions = []
            for(question_number in this.questions){
                if(this.questions[question_number].type == 'enum'){
                    for(variant_number in this.questions[question_number].variants){
                        variant = this.questions[question_number].variants[variant_number]
                        if(variant.value != ""){
                            this.questions[question_number].params.options[variant.text] = variant.value
                        }
                    }
                }
                else if(this.questions[question_number].type == 'checkbox'){
                    this.questions[question_number].params.options = this.questions[question_number].checker
                }
                let temp_add = JSON.parse(JSON.stringify(this.questions[question_number]))
                delete temp_add.variants
                delete temp_add.checker
                result_questions.push(temp_add)
            }

            this.json.fields = result_questions
            this.json.name = this.name
            this.json = JSON.stringify(this.json)


            fetch('', {
              method: 'POST',
              headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
              },
              body: this.json
            }).then(res => res.json())
              .then(function(res){
                if(res.state == "ok"){
                    alert('Анкета успешно сохранена как "' + res.name + '" (id: ' + res.id + ')')
                    window.location.href = "/editor"
                }
                else{
                    alert("Ошибка при сохранении анкеты\n" + res.state)
                }
              });


        },

        deleteQuestion(question_number){
            this.questions.splice(question_number, 1)
        },

        go_up(question_number){
            if(question_number != 0){
                let temp = JSON.parse(JSON.stringify(this.questions[question_number - 1]))
                this.questions[question_number - 1] = JSON.parse(JSON.stringify(this.questions[question_number]))
                this.questions[question_number] = temp
            }
        },

        go_down(question_number){
            if (question_number!= this.questions.length - 1 && this.questions[question_number + 1]!= undefined){
                let temp = JSON.parse(JSON.stringify(this.questions[question_number + 1]))
                this.questions[question_number + 1] = JSON.parse(JSON.stringify(this.questions[question_number]))
                this.questions[question_number] = temp
            }
        },
        openProject: function (project) {
            this.managers.project.open(project)
        }
    },
      async mounted() {
          this.event_bus.on("change-screen", async(screen) => {
            if(screen === "editor"){
                console.log()
            }
       })
  }
}

</script>



<style>
        *{
    font-family: Roboto, sans-serif;
}

.col{
    border: 1px solid transparent;
    padding: 5px;
}

.main-card{
    border: rgba(0, 0, 0, 0.3) 1px solid;
    border-radius: 5px;
}

.text{
    font-size: 12pt;
}

.bold-text{
    font-weight: bold;
}

.change_number_button{
    border: none;
    background: white;
    color: darkgrey;
    font-size: 20pt;
    font-weight: normal;
}


.change_number_button:hover{
    color: blue;
    transition: all 600ms ease;
}



</style>