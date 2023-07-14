<template>
    <div class="container" id="main">
        <div class="hstack gap-3">
            <div class="me-auto"><h4 class="my-3">Вы можете выбрать анкету для редактирования или создать новую</h4></div>
            <div bis_skin_checked="1">
                <a href="create">
                    <button class="btn btn-sm btn-primary">Создать</button>
                </a>
            </div>
        </div>

        <div class="row my-2">
            <div class="col"><input type="text" placeholder="Поиск по названию или id..." class="form-control" v-model="search"></div>
        </div>

        <div class="row py-2" v-if="isLoaded">
            <template :key="part.id" v-for="part in data">
                <div class="col-sm-6 col-md-6 col-lg-4 mb-3" v-if="search != undefined && (part.name.toLowerCase().indexOf(search.toLowerCase()) != -1 || `${part.id}`.toLowerCase().indexOf(search.toLowerCase()) != -1) ">
                    <div class="card hover-card">
                        <div class="card-body">
                            <a href="{{ part.id }}" style="text-decoration: none; color: black">
                                <h5 class="card-title mt-1 mb-3">{{ part.name }}</h5>
                                <p class="my-0 font-monospace" style="color: darkgrey; font-size: 9pt">
                                    id: {{ part.id }}
                                </p>
                            </a>
                            <div class="mt-2">
                                <a href="javascript:if(confirm('Вы уверены, что хотите удалить анкету &#34;{{ part.name }}&#34;?')){window.location.href='delete/{{ part.id }}'}" class="hover-danger-href" style="font-size: 8pt; text-decoration: none">
                                    Удалить
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
export default {
  name: 'EditorAllScreen',
  components: {},
  data() {
    return{
        isLoaded: false,
        data: {},
        search: ""
    }
  },
  methods: {
    openProject: function (project) {
      this.managers.project.open(project)
    }
  },
  async mounted() {
  this.event_bus.on("change-screen", async(screen) => {
    if(screen === "editor-all"){
        let a = await fetch(process.env.VUE_APP_MAINHOST + "/editor/get_data")
        let b = await a.json()

        this.isLoaded = true
        this.data = b
    }
  })
  }
}

</script>

<style>
    .hover-card:hover{
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 2px 4px 0 rgba(0, 0, 0, 0.2);
        transition: 0.2s;
    }
    .hover-danger-href:hover{
        color: red;
        transition: 0.2s
    }
</style>