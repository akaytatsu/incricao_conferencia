axios.defaults.withCredentials = true;


var dependentes = new Vue({
    el: '#dependentes',
    delimiters: ['[[', ']]'],
    data: {
      dependentes: [],
      dependente: {
          nome: "",
          nome_cracha: "",
          grau: "",
          data_nascimento: "",
          id: null
      },
      dependente_error: {
          nome: false,
          data_nascimento: false,
          grau: false
      }
    },
    mounted: function(){
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        this.getAllDependentes();
    },
    methods: {

        getAllDependentes: function(){
            _this = this;
            let inscricao_id = document.getElementById("inscricao_id").value;
            axios.get("/api/inscricao/dependentes", { params: { inscricao_id: inscricao_id } }).then((response) => {
                _this.dependentes = response.data;
            });
        },
        brToUs: function(data){
            data = data.split("/");

            return data[2] + "-" + data[1] + "-" + data[0];
        },
        usToBr: function(data){
            data = data.split("-");

            return data[1] + "/" + data[1] + "/" + data[0];
        },
        removeDependente: function(id){
            var _this = this;
            var params = {
                inscricao: document.getElementById("inscricao_id").value,
                id: id,
            };

            if(confirm("Deseja remover esse dependente?")){
                axios.delete("/api/inscricao/dependente", { params: params }).then((response) => {
                    _this.getAllDependentes();
                });
            }
        },
        buscaDependente: function(id){
            _this = this;
            let inscricao_id = document.getElementById("inscricao_id").value;
            var params = {
                inscricao_id: inscricao_id,
                id: id
            }
            axios.get("/api/inscricao/dependente", { params: params }).then((response) => {
                _this.dependente = response.data;
                _this.dependente.data_nascimento = _this.usToBr(_this.dependente.data_nascimento);
                $("#dependente_form").modal();
            });
        },
        salvaDependente: function(){
            
            this.limpaErrors();
            var _this = this;
            var params = {
                nome: this.dependente.nome,
                nome_cracha: this.dependente.nome_cracha,
                grau: this.dependente.grau,
                data_nascimento: this.dependente.data_nascimento,
            };
            params['data_nascimento'] = this.brToUs(this.dependente.data_nascimento);
            params['inscricao'] = document.getElementById("inscricao_id").value;

            if(this.dependente.id != null && this.dependente.id != undefined){
                params['id'] = this.dependente.id;
            }

            axios.post("/api/inscricao/dependente", params).then((response) => { 

                if(response.status == 200){
                    _this.getAllDependentes();
                    _this.limpaDependente();
                    _this.limpaErrors();
                    $("#dependente_form").modal('hide');
                }

            }).catch( (error) => {      
          
                if( error.response.status == 400 ){
                    if( error.response.data.nome != null || error.response.data.nome != undefined ){
                        _this.dependente_error.nome = true;
                    }
                    if( error.response.data.data_nascimento != null || error.response.data.data_nascimento != undefined ){
                        _this.dependente_error.data_nascimento = true;
                    }
                    if( error.response.data.grau != null || error.response.data.grau != undefined ){
                        _this.dependente_error.grau = true;
                    }
                }
            });
        },
        limpaErrors: function(){
            this.dependente_error = {
                nome: false,
                data_nascimento: false,
                grau: false
            }
        },
        limpaDependente: function(){
            this.dependente = {
                nome: "",
                nome_cracha: "",
                grau: "",
                data_nascimento: "",
            };
        },
        dependentesModal: function(){
            this.limpaDependente();
            $("#dependente_form").modal();
        }

    }
  })