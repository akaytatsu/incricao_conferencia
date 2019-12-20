axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

var processo = new Vue({
    el: "#relatorio_cidade",
    delimiters: ["[[", "]]"],
    data: function () {
        return {
            conferencias: [],
            conferencia_id: null
        }
    },
    methods: {
        buscaConferencias: function(){
            var _this = this;
            axios.get("/api/conferencias").then(function (response) {
                _this.conferencias = response.data;
            });
        },
        buscaDados(loja_id = undefined) {

            _this = this;
            var params = {
                conferencia_id: this.conferencia_id
            };

            axios.post("/api/relatorios/cidades", params).then(function (response) {
                
            });
        }
    },

    mounted() {
        this.buscaConferencias();
    }
});