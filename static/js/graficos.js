// Função para formatar moeda
function formatarMoeda(valor){
    return "R$ " + Number(valor).toLocaleString("pt-BR", {
        minimumFractionDigits: 2
    });
}


// Criar gráficos do dashboard
function criarGraficosDashboard(receita, despesa, ativo, passivo, patrimonio, fluxo){

    if(typeof Chart === "undefined"){
        console.warn("Chart.js não carregado");
        return;
    }

    Chart.defaults.font.family = "Segoe UI";
    Chart.defaults.color = "#2d3436";


    // ==============================
    // RECEITA VS DESPESA
    // ==============================

    const ctx1 = document.getElementById("receitaDespesaChart");

    if(ctx1){

        new Chart(ctx1.getContext("2d"),{

            type:"bar",

            data:{
                labels:["Receita","Despesa"],

                datasets:[{
                    label:"Financeiro",

                    data:[receita,despesa],

                    backgroundColor:[
                        "#2ecc71",
                        "#e74c3c"
                    ],

                    borderRadius:8,
                    barThickness:60
                }]
            },

            options:{

                responsive:true,

                plugins:{
                    legend:{
                        display:false
                    },

                    tooltip:{
                        callbacks:{
                            label:(ctx)=> formatarMoeda(ctx.raw)
                        }
                    }
                },

                scales:{
                    y:{
                        beginAtZero:true,
                        ticks:{
                            callback:(value)=> formatarMoeda(value)
                        }
                    }
                }

            }

        });

    }



    // ==============================
    // BALANÇO
    // ==============================

    const ctx2 = document.getElementById("balancoChart");

    if(ctx2){

        new Chart(ctx2.getContext("2d"),{

            type:"doughnut",

            data:{
                labels:[
                    "Ativo",
                    "Passivo",
                    "Patrimônio"
                ],

                datasets:[{

                    data:[
                        ativo,
                        passivo,
                        patrimonio
                    ],

                    backgroundColor:[
                        "#3498db",
                        "#e67e22",
                        "#9b59b6"
                    ],

                    borderWidth:0
                }]
            },

            options:{

                responsive:true,

                plugins:{
                    legend:{
                        position:"bottom"
                    },

                    tooltip:{
                        callbacks:{
                            label:(ctx)=>{
                                return ctx.label + ": " + formatarMoeda(ctx.raw);
                            }
                        }
                    }
                }

            }

        });

    }



    // ==============================
    // FLUXO DE CAIXA
    // ==============================

    const ctx3 = document.getElementById("fluxoChart");

    if(ctx3){

        const gradient = ctx3
            .getContext("2d")
            .createLinearGradient(0,0,0,400);

        gradient.addColorStop(0,"rgba(46,204,113,0.6)");
        gradient.addColorStop(1,"rgba(46,204,113,0.05)");

        new Chart(ctx3.getContext("2d"),{

            type:"line",

            data:{
                labels:["Saldo Atual"],

                datasets:[{

                    label:"Fluxo de Caixa",

                    data:[fluxo],

                    borderColor:"#2ecc71",

                    backgroundColor:gradient,

                    tension:0.4,

                    fill:true,

                    pointRadius:6
                }]
            },

            options:{

                responsive:true,

                plugins:{
                    legend:{
                        display:false
                    },

                    tooltip:{
                        callbacks:{
                            label:(ctx)=> formatarMoeda(ctx.raw)
                        }
                    }
                },

                scales:{
                    y:{
                        ticks:{
                            callback:(value)=> formatarMoeda(value)
                        }
                    }
                }

            }

        });

    }

}