axios.defaults.withCredentials = true;


var pagamento = new Vue({
    el: '#pagar',
    delimiters: ['[[', ']]'],
    data: {
        
    },
    mounted: function(){
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    },
    methods: {
        
        buscaCodigo: function(){
            _this = this;

            let inscricao_id = document.getElementById("inscricao_id").value;
            let conferencia_id = document.getElementById("conferencia_id").value;

            var params = {
                inscricao: parseInt(inscricao_id),
                conferencia: parseInt(conferencia_id)
            };

            axios.post('/api/pagamento', params).then(response => {
                _this.lightBox( response.data.code );
            });
        },
        lightBox: function(codigo){

            var code = codigo;
            var callback = {
                success : function(transactionCode) {
                    //Insira os comandos para quando o usuário finalizar o pagamento. 
                    //O código da transação estará na variável "transactionCode"
                    console.log("Compra feita com sucesso, código de transação: " + transactionCode);
                },
                abort : function() {
                    //Insira os comandos para quando o usuário abandonar a tela de pagamento.
                    console.log("abortado");
                }
            };
            //Chamada do lightbox passando o código de checkout e os comandos para o callback
            var isOpenLightbox = PagSeguroLightbox(code, callback);
            // Redireciona o comprador, caso o navegador não tenha suporte ao Lightbox
            if (!isOpenLightbox){
                location.href="https://pagseguro.uol.com.br/v2/checkout/payment.html?code=" + code;
                console.log("Redirecionamento")
            }
        }

    }
  })