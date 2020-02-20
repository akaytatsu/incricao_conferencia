axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

var processo = new Vue({
    el: "#relatorio_cracha",
    delimiters: ["[[", "]]"],
    data: function () {
        return {
            conferencias: [],
            registros: [],
            conferencia_id: null,

        }
    },
    methods: {
        buscaConferencias: function(){
            var _this = this;
            axios.get("/api/inscricao/conferencias").then(function (response) {
                _this.conferencias = response.data;
            });
        },
    },

    mounted() {
        this.buscaConferencias();
    }
});