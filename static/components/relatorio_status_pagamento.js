axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

var processo = new Vue({
    el: "#relatorio_status_pagamento",
    delimiters: ["[[", "]]"],
    data: function () {
        return {
            conferencias: [],
            registros: [],
            conferencia_id: null
        }
    },
    methods: {
        buscaConferencias: function(){
            var _this = this;
            axios.get("/api/inscricao/conferencias").then(function (response) {
                _this.conferencias = response.data;
            });
        },
        buscaDados(loja_id = undefined) {

            _this = this;
            var params = {
                conferencia_id: this.conferencia_id
            };

            axios.post("/api/inscricao/relatorios/status_pagamento", params).then(function (response) {
                _this.registros = response.data;
            });
        },
        getLink: function(idStatus){
            var response = "/admin/data/inscricao/?status__exact="+idStatus+"&conferencia_id=" + this.conferencia_id;

            return encodeURI(response);
        }
    },

    mounted() {
        this.buscaConferencias();
    }
});