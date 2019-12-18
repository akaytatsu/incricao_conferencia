axios.defaults.withCredentials = true;


var dependentes = new Vue({
    el: '#contato',
    delimiters: ['[[', ']]'],
    data: {
      inscricao: {
          nome: "",
          email: ""
      },
      errors: {
          nome: [],
          email: [],
          descricao: [],
          assunto: []
      }
    },
    mounted: function(){
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        this.getData();
    },
    methods: {
        
        cleanErrors: function(){
            this.errors = {
                nome: [],
                email: [],
                descricao: [],
                assunto: []
            }
        },
        getData: function(){
            _this = this;
            let inscricao_id = document.getElementById("inscricao_id").value;
            axios.get("/api/inscricao", { params: { inscricao_id: inscricao_id } }).then((response) => {
                _this.inscricao = response.data;
            });
        },
        enviaContato: function(){
            _this = this;
            let inscricao_id = document.getElementById("inscricao_id").value;
            let conferencia_id = document.getElementById("conferencia_id").value;

            var params = {
                nome: this.inscricao.nome,
                email: this.inscricao.email,
                assunto: this.inscricao.assunto,
                descricao: this.inscricao.descricao,
                inscricao: parseInt(inscricao_id),
                conferencia: parseInt(conferencia_id)
            };

            axios.post("/api/contato", params ).then((response) => {
                _this.getData();
                _this.cleanErrors();
                alert("Recebemos seus dados. Em breve entraremos em contato.");
            }).catch((error) => {
                _this.errors = error.response.data;
            });
        }

    }
  })