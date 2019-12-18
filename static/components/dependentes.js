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
        this.getData();
    },
    methods: {

        getData: function(){
            _this = this;
            let inscricao_id = document.getElementById("inscricao_id").value;
            axios.get("/api/dependentes", { params: { inscricao_id: inscricao_id } }).then((response) => {
                _this.dependentes = response.data;
            });
        },
        salvaDependente: function(){
            
            this.limpaErrors();
            var _this = this;
            var params = this.dependente;
            params['inscricao'] = document.getElementById("inscricao_id").value;
            axios.post("/api/dependentes", params).then((response) => {

                if( response.status == 400 ){
                    console.log(response.data);
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